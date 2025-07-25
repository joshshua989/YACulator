# config.py

# -------------------------------
# File Paths
# -------------------------------
NFL_SCHEDULE_FILE = "NFL_SCHEDULE_2025.csv"
ADV_WR_STATS_FILE = "ADVANCED_WR_STATS_2024.csv"
CB_ALIGNMENT_FILE = "CB_ALIGNMENT.csv"
DEF_COVERAGE_TAGS_FILE = "DEF_COVERAGE_TAGS.csv"
ROSTER_2025_FILE = "roster_2025.csv"
ROSTER_2024_FILE = "roster_2024.csv"  # Fallback if 2025 is missing

# -------------------------------
# Projection Weights
# -------------------------------
SLOT_WEIGHT_MULTIPLIER = 1.0
WIDE_WEIGHT_MULTIPLIER = 1.0
SAFETY_WEIGHT_MULTIPLIER = 0.2
LB_WEIGHT_MULTIPLIER = 0.1

# -------------------------------
# Coverage Scheme Logic
# -------------------------------
DEFAULT_MAN_ZONE_BLEND = True  # Blend man/zone usage if no hard split

# -------------------------------
# Multi-Year Blend Decay
# -------------------------------
WEIGHT_2024 = 0.5
WEIGHT_2023 = 0.3
WEIGHT_2022 = 0.2

# -------------------------------
# Output
# -------------------------------
EXPORT_FULL_SEASON_FILE = "season_projection_output.csv"
EXPORT_TEST_WEEK_FILE = "test_week_projection.csv"

# -------------------------------
# Logging + Quality Control
# -------------------------------
ENABLE_QUALITY_CONTROL = True