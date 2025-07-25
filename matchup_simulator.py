# matchup_simulator.py
import pandas as pd
import numpy as np
from collections import defaultdict

WEEKLY_DEFENSE_CSV = "ADVSTATS_WEEK_DEF_2024.csv"
SCHEDULE_CSV = "NFL_SCHEDULE_2025.csv"
ROSTER_CSV = "roster_2024.csv"
CB_ALIGNMENT_CSV = "CB_ALIGNMENT.csv"

# --- Classes ---
class DB:
    def __init__(self, name, team, position):
        self.name = name
        self.team = team
        self.position = position  # CB, S, LB
        self.coverage_stats = {}
        self.alignment_role = None

    def load_alignment_profile(self, row):
        self.coverage_stats = {
            "targets_allowed": row.get("Targets Allowed", 0),
            "catch_rate": row.get("Catch Rate Allowed", 0),
            "passer_rating": row.get("Passer Rating Allowed", 0),
            "fpts_per_target": row.get("Fantasy Points Allowed Per Target", 0),
            "fpts_per_game": row.get("Fantasy Points Allowed Per Game", 0),
            "man_success": row.get("Man Coverage Success Rate", 0),
            "separation": row.get("Target Separation", 0)
        }
        if self.position == 'S':
            self.alignment_role = "safety"
        elif self.position == 'LB':
            self.alignment_role = "linebacker"
        elif row.get("Man Coverage Rate", 0) > 0.5:
            self.alignment_role = "wide"
        elif row.get("Catch Rate Allowed", 0) > 0.7:
            self.alignment_role = "slot"
        else:
            self.alignment_role = "wide"

class WR:
    def __init__(self, name, position, team):
        self.name = name
        self.position = position
        self.team = team
        self.role = None
        self.slot_snap_rate = 0.0
        self.is_slot = False
        self.vs_man = {}
        self.vs_zone = {}
        self.weekly_stats = {}

    
    def load_alignment_and_coverage(self, row):
        self.slot_snap_rate = row.get("SlotSnapRate", 0)
        self.snap_share = row.get("SnapShare", 0)
        self.routes_run = row.get("RoutesRun", 0)
        self.wide_snap_rate = 1.0 - self.slot_snap_rate

        # Alignment weights for projections
        self.alignment_weights = {
            "slot": self.slot_snap_rate,
            "wide": self.wide_snap_rate,
            "safety": 0.2 if self.slot_snap_rate > 0.3 else 0.05,
            "lb": 0.1 if self.slot_snap_rate > 0.2 else 0.0
        }

        self.vs_man = {
            "routes": row.get("RoutesVsMan", 0),
            "win_rate": row.get("WinRateVsMan", 0),
            "target_rate": row.get("TargetRateVsMan", 0),
            "separation": row.get("TargetSeparationVsMan", 0),
            "fpts_per_target": row.get("FantasyPointsPerTargetVsMan", 0)
        }

        self.vs_zone = {
            "routes": row.get("RoutesVsZone", 0),
            "win_rate": row.get("WinRateVsZone", 0),
            "target_rate": row.get("TargetRateVsZone", 0),
            "separation": row.get("TargetSeparationVsZone", 0),
            "fpts_per_target": row.get("FantasyPointsPerTargetVsZone", 0)
        }

    f = pd.read_csv(filepath)
    db_map = defaultdict(dict)
    for _, row in df.iterrows():
        name = row['PlayerYear']
        team = row['Team']
        pos = row['Position']
        db = DB(name, team, pos)
        db.load_alignment_profile(row)
        db_map[team][name] = db
    return db_map

def load_wr_advanced_stats(filepath="ADVANCED_WR_STATS_2024.csv"):
    df = pd.read_csv(filepath)
    wrs = {}
    for _, row in df.iterrows():
        name = row['Player']
        team = row['Team']
        wr = WR(name, 'WR', team)
        wr.load_alignment_and_coverage(row)
        wrs[name] = wr
    return wrs

# --- Matchup Simulation ---
def project_wr_week(wr, week, schedule_df, db_alignment_map, coverage_map):
    matchup_row = schedule_df[(schedule_df['week'] == week) & (schedule_df['team'] == wr.team)]
    if matchup_row.empty:
        return None

    opp_team = matchup_row.iloc[0]['opponent']
    scheme = coverage_map[week][opp_team]
    db_pool = db_alignment_map.get(opp_team, {})
    if not db_pool:
        return None

    slot_dbs = [db for db in db_pool.values() if db.alignment_role == 'slot']
    wide_dbs = [db for db in db_pool.values() if db.alignment_role == 'wide']
    safety_dbs = [db for db in db_pool.values() if db.alignment_role == 'safety']
    lb_dbs = [db for db in db_pool.values() if db.alignment_role == 'linebacker']

    def avg_db_penalty(dbs):
        if not dbs:
            return 1.0
        penalties = []
        for db in dbs:
            stats = db.coverage_stats
            penalty = (stats['catch_rate'] / 100.0 + stats['separation'] / 3.0 + stats['passer_rating'] / 158.3) / 3
            penalties.append(penalty)
        return np.mean(penalties)

    slot_weight = wr.slot_snap_rate
    wide_weight = 1.0 - slot_weight
    safety_weight = 0.2 if scheme == 'zone' else 0.05
    lb_weight = 0.1 if scheme == 'zone' else 0.0

    base_pts = wr.vs_man['fpts_per_target'] if scheme == 'man' else wr.vs_zone['fpts_per_target']

    slot_penalty = avg_db_penalty(slot_dbs)
    wide_penalty = avg_db_penalty(wide_dbs)
    safety_penalty = avg_db_penalty(safety_dbs)
    lb_penalty = avg_db_penalty(lb_dbs)

    total_weight = slot_weight + wide_weight + safety_weight + lb_weight
    adjusted_pts = base_pts * (
        slot_weight * (1 - slot_penalty) +
        wide_weight * (1 - wide_penalty) +
        safety_weight * (1 - safety_penalty) +
        lb_weight * (1 - lb_penalty)
    ) / total_weight

    top_matchups = sorted(db_pool.values(), key=lambda db: db.coverage_stats.get('targets_allowed', 0), reverse=True)[:3]

    return {
        'week': week,
        'wr_name': wr.name,
        'team': wr.team,
        'opp_team': opp_team,
        'scheme': scheme,
        'base_pts': round(base_pts, 2),
        'adj_pts': round(adjusted_pts, 2),
        'slot_weight': round(slot_weight, 2),
        'wide_weight': round(wide_weight, 2),
        'safety_weight': round(safety_weight, 2),
        'lb_weight': round(lb_weight, 2),
        'top_defenders': [d.name for d in top_matchups]
    }
