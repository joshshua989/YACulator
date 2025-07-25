# sim_engine.py

import pandas as pd
from config import (
    NFL_SCHEDULE_2025_FILE,
    WR_STATS_2024_FILE,
    DB_ALIGNMENT_FILE,
    DEF_COVERAGE_TAGS_FILE,
    EXPORT_FULL_SEASON_FILE,
    EXPORT_TEST_WEEK_FILE,
)
from stat_loader import load_csv
from matchup_simulator import load_db_alignment, load_wr_stats, project_wr_week


def build_def_coverage_map(coverage_df):
    def_coverage_map = {}
    for _, row in coverage_df.iterrows():
        week = row['week']
        team = row['team']
        if week not in def_coverage_map:
            def_coverage_map[week] = {}
        def_coverage_map[week][team] = (
            "man" if row.get("man_coverage_rate", 0) >= row.get("zone_coverage_rate", 0) else "zone"
        )
    return def_coverage_map


def run_test_week_simulation(week, output_file=None):
    schedule_df = load_csv(NFL_SCHEDULE_2025_FILE)
    wr_map = load_wr_stats(WR_STATS_2024_FILE)
    db_map = load_db_alignment(DB_ALIGNMENT_FILE)
    coverage_df = load_csv(DEF_COVERAGE_TAGS_FILE)
    def_coverage_map = build_def_coverage_map(coverage_df)

    results = []
    for wr in wr_map.values():
        proj = project_wr_week(wr, week, schedule_df, db_map, def_coverage_map)
        if proj:
            results.append(proj)

    output_df = pd.DataFrame(results)
    out_file = output_file or EXPORT_TEST_WEEK_FILE
    output_df.to_csv(out_file, index=False)
    print(f"✅ Test Week {week} projections saved to {out_file}")


def run_season_simulation(output_file=None):
    print(f'\n1. Loading {NFL_SCHEDULE_2025_FILE}...')
    schedule_df = load_csv(NFL_SCHEDULE_2025_FILE)
    print(f'\n2. Loading {WR_STATS_2024_FILE}...')
    wr_map = load_wr_stats(WR_STATS_2024_FILE)
    print(f'\n3. Loading {DB_ALIGNMENT_FILE}...')
    db_map = load_db_alignment(DB_ALIGNMENT_FILE)
    print(f'\n4. Loading {DEF_COVERAGE_TAGS_FILE}...')
    coverage_df = load_csv(DEF_COVERAGE_TAGS_FILE)
    print(f'\n5. Building {EXPORT_FULL_SEASON_FILE}...')
    def_coverage_map = build_def_coverage_map(coverage_df)

    results = []
    for week in schedule_df['Week'].unique():
        for wr in wr_map.values():
            proj = project_wr_week(wr, week, schedule_df, db_map, def_coverage_map)
            if proj:
                results.append(proj)

    output_df = pd.DataFrame(results)
    out_file = output_file or EXPORT_FULL_SEASON_FILE
    output_df.to_csv(out_file, index=False)
    print(f"\n✅ Full-season projections saved to {out_file}")
