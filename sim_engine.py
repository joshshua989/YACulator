
# sim_engine.py

import pandas as pd
from config import (
    NFL_SCHEDULE_2025_FILE,
    WR_STATS_2024_FILE,
    DB_ALIGNMENT_FILE,
    DEF_COVERAGE_TAGS_FILE,
    EXPORT_FULL_SEASON_FILE,
    EXPORT_TEST_WEEK_FILE,
    STADIUM_ENV_FILE
)
from stat_loader import load_csv
from matchup_simulator import load_db_alignment, load_wr_stats, project_wr_week
from weather_boost_generator import build_weather_boost_map
from multiprocessing import Pool, cpu_count


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


def run_test_week_simulation(week, output_file=None, simulations=100):
    schedule_df = load_csv(NFL_SCHEDULE_2025_FILE)
    wr_map = load_wr_stats(WR_STATS_2024_FILE)
    db_map = load_db_alignment(DB_ALIGNMENT_FILE)
    coverage_df = load_csv(DEF_COVERAGE_TAGS_FILE)
    def_coverage_map = build_def_coverage_map(coverage_df)
    env_profile_df = load_csv(STADIUM_ENV_FILE)
    env_boost_map = build_weather_boost_map(schedule_df)

    results = []
    penalty_cache = {}

    for wr in wr_map.values():
        key = (week, wr.team)
        if key not in penalty_cache:
            penalty_cache[key] = None
        proj = project_wr_week(
            wr, week, schedule_df, db_map, def_coverage_map,
            simulations=simulations,
            precomputed=penalty_cache[key],
            env_boost_map=env_boost_map
        )
        if proj:
            results.append(proj)

    output_df = pd.DataFrame(results)
    out_file = output_file or EXPORT_TEST_WEEK_FILE
    output_df.to_csv(out_file, index=False)
    print(f"✅ Test Week {week} projections saved to {out_file}")


def simulate_for_week(args):
    week, wr_map, schedule_df, db_map, def_coverage_map, env_boost_map, simulations = args
    penalty_cache = {}
    results = []
    for wr in wr_map.values():
        key = (week, wr.team)
        if key not in penalty_cache:
            penalty_cache[key] = None
        proj = project_wr_week(
            wr, week, schedule_df, db_map, def_coverage_map,
            simulations=simulations,
            precomputed=penalty_cache[key],
            env_boost_map=env_boost_map
        )
        if proj:
            results.append(proj)
    return results


def run_season_simulation(output_file=None, simulations=100):
    print(f'\n1. Loading schedule...')
    schedule_df = load_csv(NFL_SCHEDULE_2025_FILE)

    print(f'\n2. Loading WR stats...')
    wr_map = load_wr_stats(WR_STATS_2024_FILE)

    print(f'\n3. Loading DB alignment...')
    db_map = load_db_alignment(DB_ALIGNMENT_FILE)

    print(f'\n4. Loading coverage tags...')
    coverage_df = load_csv(DEF_COVERAGE_TAGS_FILE)
    def_coverage_map = build_def_coverage_map(coverage_df)

    print(f'\n5. Loading environment profile...')
    env_profile_df = load_csv(STADIUM_ENV_FILE)
    env_boost_map = build_weather_boost_map(schedule_df)

    print(f'\n6. Simulating season in parallel using {cpu_count()} cores...')
    args = [
        (week, wr_map, schedule_df, db_map, def_coverage_map, env_boost_map, simulations)
        for week in sorted(schedule_df['Week'].unique())
    ]

    with Pool(cpu_count()) as pool:
        week_results = pool.map(simulate_for_week, args)

    results = [r for week in week_results for r in week if r]

    output_df = pd.DataFrame(results)
    out_file = output_file or EXPORT_FULL_SEASON_FILE
    output_df.to_csv(out_file, index=False)
    print(f"\n✅ Full-season projections saved to {out_file}")

    team_summary = output_df.groupby(['team']).agg({
        'adj_pts': ['sum', 'mean'],
        'adj_pts_p50': 'mean' if 'adj_pts_p50' in output_df.columns else 'mean',
        'base_pts': 'mean'
    }).reset_index()
    team_summary.columns = ['Team', 'Total Adj Pts', 'Avg Adj Pts', 'Avg Median Pts', 'Avg Base Pts']
    team_summary.to_csv("output/team_projection_summary.csv", index=False)
    print("📊 Team summary saved to output/team_projection_summary.csv")
