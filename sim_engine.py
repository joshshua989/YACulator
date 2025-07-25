
# sim_engine.py
import pandas as pd
from config import (
    NFL_SCHEDULE_FILE,
    ADV_WR_STATS_FILE,
    CB_ALIGNMENT_FILE,
    DEF_COVERAGE_TAGS_FILE,
    EXPORT_FULL_SEASON_FILE
)
from stat_loader import load_csv
from matchup_simulator import load_db_alignment, load_wr_advanced_stats, project_wr_week

def run_full_season_simulation():
    schedule_df = load_csv(NFL_SCHEDULE_FILE)
    wr_map = load_wr_advanced_stats(ADV_WR_STATS_FILE)
    db_map = load_db_alignment(CB_ALIGNMENT_FILE)
    coverage_df = load_csv(DEF_COVERAGE_TAGS_FILE)

    # Build defensive scheme lookup
    def_coverage_map = {}
    for _, row in coverage_df.iterrows():
        week = row["week"]
        team = row["team"]
        if week not in def_coverage_map:
            def_coverage_map[week] = {}
        # Weighted logic for man/zone
        scheme = "man" if row["man_coverage_rate"] >= row["zone_coverage_rate"] else "zone"
        def_coverage_map[week][team] = scheme

    all_results = []
    for week in sorted(schedule_df["week"].unique()):
        for wr in wr_map.values():
            proj = project_wr_week(wr, week, schedule_df, db_map, def_coverage_map)
            if proj:
                all_results.append(proj)

    output_df = pd.DataFrame(all_results)
    output_df.to_csv(EXPORT_FULL_SEASON_FILE, index=False)
    print(f"[✓] Full season projection saved to: {EXPORT_FULL_SEASON_FILE}")
    return output_df
