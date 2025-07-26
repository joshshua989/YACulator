# config.py

# -------------------------------
# File Paths
# -------------------------------
NFL_SCHEDULE_2025_FILE = "DATA/NFL_SCHEDULE_2025.csv"
WR_STATS_2024_FILE = "DATA/WR_STATS_2024.csv"
DB_ALIGNMENT_FILE = "DATA/DB_STATS_2022_2023_2024.csv"
DEF_COVERAGE_TAGS_FILE = "DEF_COVERAGE_TAGS.csv"
ROSTER_2025_FILE = "roster_2025.csv"
ROSTER_2024_FILE = "roster_2024.csv"  # Fallback if 2025 is missing
BLENDED_WR_FILE = "BLENDED_WR_STATS.csv"
BLENDED_DB_FILE = "BLENDED_DB_STATS.csv"
STADIUM_ENV_FILE = "DATA/STADIUM_ENVIRONMENT_PROFILES.csv"

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

# -------------------------------
# Alignment Logic
# -------------------------------
USE_SOFT_ALIGNMENT = True  # Enable probabilistic DB role assignment

# -------------------------------
# Environment Settings
# -------------------------------
FORCE_DOME_NO_WEATHER_PENALTY = True
CLIMATE_PHASE = "Neutral"  # Options: "ElNino", "LaNina", "Neutral"
USE_FORECAST_WEATHER = True
