
# main.py

from config import (
    NFL_SCHEDULE_FILE,
    ADV_WR_STATS_FILE,
    CB_ALIGNMENT_FILE,
    DEF_COVERAGE_TAGS_FILE,
    EXPORT_FULL_SEASON_FILE,
)
from stat_loader import load_csv
from matchup_simulator import load_db_alignment, load_wr_advanced_stats, project_wr_week
import pandas as pd

def run_full_season():
    schedule_df = load_csv(NFL_SCHEDULE_FILE)
    wr_map = load_wr_advanced_stats(ADV_WR_STATS_FILE)
    db_map = load_db_alignment(CB_ALIGNMENT_FILE)
    coverage_df = load_csv(DEF_COVERAGE_TAGS_FILE)

    # Build coverage map
    def_coverage_map = {}
    for _, row in coverage_df.iterrows():
        week = row['week']
        team = row['team']
        if week not in def_coverage_map:
            def_coverage_map[week] = {}
        if row.get("man_coverage_rate", 0) >= row.get("zone_coverage_rate", 0):
            def_coverage_map[week][team] = "man"
        else:
            def_coverage_map[week][team] = "zone"

    results = []
    for week in schedule_df['week'].unique():
        for wr in wr_map.values():
            proj = project_wr_week(wr, week, schedule_df, db_map, def_coverage_map)
            if proj:
                results.append(proj)

    output_df = pd.DataFrame(results)
    output_df.to_csv(EXPORT_FULL_SEASON_FILE, index=False)
    print(f"✅ Full-season projections written to {EXPORT_FULL_SEASON_FILE}")

if __name__ == "__main__":
    run_full_season()
