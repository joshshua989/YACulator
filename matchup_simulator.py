# YACulator: matchup_simulator.py
import pandas as pd
import numpy as np
from collections import defaultdict
from config import (
    SLOT_WEIGHT_MULTIPLIER,
    WIDE_WEIGHT_MULTIPLIER,
    SAFETY_WEIGHT_MULTIPLIER,
    LB_WEIGHT_MULTIPLIER,
    DEFAULT_MAN_ZONE_BLEND,
    BLENDED_DB_FILE,
    BLENDED_WR_FILE,
)

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
            # If the player's position is a Safety ('S'), they're automatically labeled as "safety", regardless of coverage stats.
            self.alignment_role = "safety"
        elif self.position == 'LB':
            self.alignment_role = "linebacker"
        elif row.get("Man Coverage Rate", 0) > 0.5:
            # If the DB is not a safety and their man coverage rate is over 50%, we assume they often play outside (wide) where man coverage is more common.
            self.alignment_role = "wide"
        elif row.get("Catch Rate Allowed", 0) > 0.7:
            # If their catch rate allowed is greater than 70%, it's assumed they're likely a slot corner (since slot defenders often face quick, high-efficiency routes that lead to high catch rates).
            self.alignment_role = "slot"
        else:
            # Default case: if none of the above conditions apply, assign them as "wide" (outside CB).
            self.alignment_role = "wide"

class WR:
    def __init__(self, name, position, team):
        self.name = name
        self.position = position
        self.team = team
        self.role = None
        self.slot_snap_rate = 0.0
        self.wide_snap_rate = 0.0
        self.snap_share = 0.0
        self.routes_run = 0
        self.is_slot = False
        self.alignment_weights = {}
        self.weekly_stats = {}
        self.vs_man = {}
        self.vs_zone = {}

    def load_alignment_and_coverage(self, row):
        self.slot_snap_rate = row.get("SlotSnapRate", 0)
        self.snap_share = row.get("SnapShare", 0)
        self.routes_run = row.get("RoutesRun", 0)
        self.wide_snap_rate = 1.0 - self.slot_snap_rate

        self.alignment_weights = {
            "slot": self.slot_snap_rate * SLOT_WEIGHT_MULTIPLIER,
            "wide": self.wide_snap_rate * WIDE_WEIGHT_MULTIPLIER,
            "safety": (0.2 if self.slot_snap_rate > 0.3 else 0.05) * SAFETY_WEIGHT_MULTIPLIER,
            "lb": (0.1 if self.slot_snap_rate > 0.2 else 0.0) * LB_WEIGHT_MULTIPLIER
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

# --- Loaders ---
def load_db_alignment(filepath=BLENDED_DB_FILE):
    df = pd.read_csv(filepath)
    db_map = defaultdict(dict)
    sample_printed = False

    for _, row in df.iterrows():
        name = row['PlayerYear']
        team = row['Team']
        pos = row['Position']
        db = DB(name, team, pos)
        db.load_alignment_profile(row)
        db_map[team][name] = db

        # Print first sample row
        if not sample_printed:
            print(f"\n(SAMPLE) {filepath}:")
            print(f"🔍 DB Name: {db.name}")
            print(f"🏈 Team: {db.team}")
            print(f"📌 Position: {db.position}")
            print(f"🎯 Role: {db.alignment_role}")
            print("📊 Coverage Stats:")
            for k, v in db.coverage_stats.items():
                print(f"   - {k}: {v}")
            sample_printed = True

    return db_map

def load_wr_stats(filepath=BLENDED_WR_FILE):
    df = pd.read_csv(filepath)
    wrs = {}
    sample_printed = False

    for _, row in df.iterrows():
        name = row['Player']
        team = row['Team']
        wr = WR(name, 'WR', team)
        wr.load_alignment_and_coverage(row)
        wrs[name] = wr

        # Print first sample row
        if not sample_printed:
            print(f'\n(SAMPLE) {filepath}:')
            print(f"🔍 WR Name: {wr.name}")
            print(f"🏈 Team: {wr.team}")
            print(f"📌 Position: {wr.position}")
            print(f"📊 Slot Snap Rate: {wr.slot_snap_rate}")

            print("\n🛡️ vs Man Coverage:")
            for k, v in wr.vs_man.items():
                print(f"  - {k}: {v}")

            print("\n🛡️ vs Zone Coverage:")
            for k, v in wr.vs_zone.items():
                print(f"  - {k}: {v}")
            sample_printed = True

    print("")
    print(wrs.keys())

    return wrs

# --- WR-to-DB Projection ---
def project_wr_week(wr, week, schedule_df, db_alignment_map, coverage_map):
    # Match WR's team in either Home or Visitor column
    matchup_row = schedule_df[
        (schedule_df['Week'] == week) &
        ((schedule_df['Visitor'] == wr.team) | (schedule_df['Home'] == wr.team))
        ]

    if matchup_row.empty:
        return None

    row = matchup_row.iloc[0]
    opp_team = row['Home'] if row['Visitor'] == wr.team else row['Visitor']

    # Get coverage scheme for opponent
    scheme = coverage_map.get(week, {}).get(opp_team, "man" if DEFAULT_MAN_ZONE_BLEND else "unknown")

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

    slot_weight = wr.alignment_weights.get('slot', 0.0)
    wide_weight = wr.alignment_weights.get('wide', 0.0)
    safety_weight = wr.alignment_weights.get('safety', 0.0)
    lb_weight = wr.alignment_weights.get('lb', 0.0)
    total_weight = slot_weight + wide_weight + safety_weight + lb_weight

    base_pts = wr.vs_man['fpts_per_target'] if scheme == 'man' else wr.vs_zone['fpts_per_target']
    slot_penalty = avg_db_penalty(slot_dbs)
    wide_penalty = avg_db_penalty(wide_dbs)
    safety_penalty = avg_db_penalty(safety_dbs)
    lb_penalty = avg_db_penalty(lb_dbs)

    adjusted_pts = base_pts * (
            slot_weight * (1 - slot_penalty) +
            wide_weight * (1 - wide_penalty) +
            safety_weight * (1 - safety_penalty) +
            lb_weight * (1 - lb_penalty)
    ) / total_weight

    top_matchups = sorted(db_pool.values(), key=lambda db: db.coverage_stats.get('targets_allowed', 0), reverse=True)[
                   :3]

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
    
