# YACulator: multi_year_blend.py
import pandas as pd
import os
from config import *

def load_wr_data():
    wr_2024 = pd.read_csv("ADVANCED_WR_STATS_2024.csv")
    wr_2023 = pd.read_csv("ADVANCED_WR_STATS_2023.csv")
    wr_2022 = pd.read_csv("ADVANCED_WR_STATS_2022.csv")
    return wr_2024, wr_2023, wr_2022

def blend_wr_stats():
    wr24, wr23, wr22 = load_wr_data()
    common_cols = list(set(wr24.columns) & set(wr23.columns) & set(wr22.columns))
    wr = wr24[common_cols].copy()
    wr.set_index("Player", inplace=True)

    for col in common_cols:
        if col != "Player":
            wr[col] = (
                WEIGHT_2024 * wr24.set_index("Player")[col] +
                WEIGHT_2023 * wr23.set_index("Player")[col] +
                WEIGHT_2022 * wr22.set_index("Player")[col]
            )
    wr.reset_index().to_csv(BLENDED_WR_FILE, index=False)
    print(f"✅ Saved blended WR stats to {BLENDED_WR_FILE}")

if __name__ == "__main__":
    blend_wr_stats()
