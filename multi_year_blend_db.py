# YACulator: multi_year_blend_db.py

import pandas as pd
import argparse
from config import (
    WEIGHT_2024, WEIGHT_2023, WEIGHT_2022,
    BLENDED_DB_FILE
)

def load_db_data():
    db_2024 = pd.read_csv("CB_ALIGNMENT_2024.csv")
    db_2023 = pd.read_csv("CB_ALIGNMENT_2023.csv")
    db_2022 = pd.read_csv("CB_ALIGNMENT_2022.csv")
    return db_2024, db_2023, db_2022

def blend_db_stats():
    db24, db23, db22 = load_db_data()
    common_cols = list(set(db24.columns) & set(db23.columns) & set(db22.columns))
    db = db24[common_cols].copy()
    db.set_index("PlayerYear", inplace=True)

    for col in common_cols:
        if col != "PlayerYear":
            db[col] = (
                WEIGHT_2024 * db24.set_index("PlayerYear")[col] +
                WEIGHT_2023 * db23.set_index("PlayerYear")[col] +
                WEIGHT_2022 * db22.set_index("PlayerYear")[col]
            )

    db.reset_index().to_csv(BLENDED_DB_FILE, index=False)
    print(f"✅ Saved blended DB stats to {BLENDED_DB_FILE}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Blend DB Stats (2022–2024)")
    parser.add_argument("--no-blend", action="store_true", help="Skip DB blending")
    args = parser.parse_args()

    if not args.no_blend:
        blend_db_stats()
    else:
        print("⚠️ Skipping DB blend due to --no-blend flag.")
