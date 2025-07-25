# main.py

import argparse
from sim_engine import run_test_week_simulation, run_season_simulation

def main():
    parser = argparse.ArgumentParser(description="Run WR Fantasy Projection Simulation")
    parser.add_argument("--mode", choices=["test", "season"], default="season", help="Which mode to run: 'test' or 'season'")
    parser.add_argument("--week", type=int, default=1, help="Week number to test (only used if mode is 'test')")
    parser.add_argument("--output", type=str, default=None, help="Optional override output file name")

    args = parser.parse_args()

    if args.mode == "test":
        print(f"🔍 Running test projection for Week {args.week}")
        run_test_week_simulation(args.week, args.output)
    else:
        print("\n📅 Running full season projection...")
        run_season_simulation(output_file=args.output)

if __name__ == "__main__":
    main()
    
