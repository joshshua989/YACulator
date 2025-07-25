import pandas as pd

# Path to your DB stats file
csv_path = "DATA/DB_STATS_2022_2023_2024.csv"

# List of expected columns
columns = [
    "Year", "Team", "Player", "Position", "IsRookie", "Height", "Weight", "ArmLength", "ArmLengthRank",
    "DraftPick", "DraftYear", "College", "GamesPlayed", "SoloTackles", "AssistedTackles", "Sacks",
    "QBPressures", "TacklesForLoss", "RunStuffs", "FantasyPointsPerGame", "SnapShare", "ManCoverageRate",
    "ShadowRate", "TargetsAllowed", "TargetRate", "RoutesDefended", "AverageTargetDistance",
    "TargetSeparation", "ReceptionsAllowed", "YardsAllowed", "YardsPerReceptionAllowed",
    "YardsPerTargetAllowed", "PassBreak-ups", "TDsAllowed", "CoverageRating", "ManCoverageSuccessRate",
    "CatchRateAllowed", "PasserRatingAllowed", "FantasyPtsAllowedPerCoverSnap",
    "FantasyPointsAllowedPerTarget", "FantasyPointsAllowedPerGame"
]

# Load CSV
df = pd.read_csv(csv_path)

# Reorder or filter to ensure we only include the columns we care about
df = df[[col for col in columns if col in df.columns]]

print("")

# Print each row nicely
for idx, row in df.iterrows():
    print(f"📅 Year: {row.get('Year', '')} | 🏈 Team: {row.get('Team', '')} | 🧍 Player: {row.get('Player', '')} | 📌 Pos: {row.get('Position', '')}")
    print("")
    print(f"   Player Build:")
    print(f"    📏 Height: {row.get('Height', '')}"
          f"    💪 Weight: {row.get('Weight', '')}"
          f"    🦾 Arm Length: {row.get('ArmLength', '')} ({row.get('ArmLengthRank', '')})")
    print("")
    print("   Draft Class:")
    print(f"    🎓 College: {row.get('College', '')}\n"
          f"       Draft: {row.get('DraftYear', '')}\n"
          f"       Pick: {row.get('DraftPick', '')}")
    print("")
    print("   Games Played:")
    print(f"    📊 Games: {row.get('GamesPlayed', '')}")
    print("")
    print("   Stat Type A:")
    print(f"     - Solo Tackles: {row.get('SoloTackles', '')}")
    print(f"     - Assisted Tackles: {row.get('AssistedTackles', '')}")
    print(f"     - Sacks: {row.get('Sacks', '')}")
    print(f"     - QB Pressures: {row.get('QBPressures')}")
    print(f"     - Tackles For Loss: {row.get('TacklesForLoss', '')}")
    print(f"     - Run Stuffs: {row.get('RunStuffs', '')}")
    print(f"     - Fantasy Points Per Game: {row.get('FantasyPointsPerGame', '')}")
    print("")
    print("   Stat Type B:")
    print(f"     - Snap Share: {row.get('SnapShare', '')}\n"
          f"     - Man Coverage Rate: {row.get('ManCoverageRate', '')}\n"
          f"     - Shadow Rate: {row.get('ShadowRate', '')}\n"
          f"     - Targets Allowed: {row.get('TargetsAllowed', '')}\n"
          f"     - Target Rate: {row.get('TargetRate', '')}\n"
          f"     - Routes Defended: {row.get('RoutesDefended', '')}\n"
          f"     - Average TargetDistance: {row.get('AverageTargetDistance', '')}\n"
          f"     - Target Separation: {row.get('TargetSeparation', '')}\n"
          f"     - Receptions Allowed: {row.get('ReceptionsAllowed', '')}\n"
          f"     - Yards Allowed: {row.get('YardsAllowed', '')}\n"
          f"     - Yards Per Reception Allowed: {row.get('YardsPerReceptionAllowed', '')}\n"
          f"     - Yards Per Target Allowed: {row.get('YardsPerTargetAllowed', '')}\n"
          f"     - Pass Break-ups: {row.get('PassBreakups', '')}\n"
          f"     - TDsAllowed: {row.get('TDsAllowed', '')}\n"
          f"     - Coverage Rating: {row.get('CoverageRating', '')}\n"
          f"     - Man Coverage Success Rate: {row.get('ManCoverageSuccessRate', '')}\n"
          f"     - Catch Rate Allowed: {row.get('CatchRateAllowed', '')}\n"
          f"     - Passer Rating Allowed: {row.get('PasserRatingAllowed', '')}\n"
          f"     - Fantasy Pts Allowed Per CoverSnap: {row.get('FantasyPtsAllowedPerCoverSnap', '')}\n"
          f"     - Fantasy Points Allowed Per Target: {row.get('FantasyPointsAllowedPerTarget', '')}\n"
          f"     - Fantasy Points Allowed Per Game: {row.get('FantaPointsAllowedPerGame', '')}\n")
    print("—" * 80)

# Optional: print total count
print(f"\n✅ Loaded {len(df)} rows.")
