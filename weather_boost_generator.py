
# weather_boost_generator.py

import requests
from datetime import datetime
from config import STADIUM_ENV_FILE, CLIMATE_PHASE
from stat_loader import load_csv
from weather_estimator import estimate_weather_boost
from config import USE_FORECAST_WEATHER

forecast_cache = {}

def get_forecast_boost(lat, lon, date):
    key = (lat, lon, date)
    if key in forecast_cache:
        return forecast_cache[key]

    try:
        point_url = f"https://api.weather.gov/points/{lat},{lon}"
        point_resp = requests.get(point_url, timeout=10)
        point_resp.raise_for_status()
        point_data = point_resp.json()
        forecast_url = point_data["properties"]["forecast"]

        forecast_resp = requests.get(forecast_url, timeout=10)
        forecast_resp.raise_for_status()
        forecast_data = forecast_resp.json()

        from dateutil import parser  # ← make sure this is imported

        try:
            parsed_date = parser.parse(date)
            target_day = parsed_date.strftime("%A")
        except Exception as e:
            print(f"⚠️ Date parsing failed for value: {date} — using default 'Sunday'")
            target_day = "Sunday"

        boost = 1.0
        condition = "Normal"

        for period in forecast_data["properties"]["periods"]:
            if period["name"] == target_day:
                temp = period.get("temperature", 60)
                wind = period.get("windSpeed", "10 mph")
                wind_speed = int(wind.split(" ")[0]) if wind else 10
                short_forecast = period.get("shortForecast", "")

                condition = f"{temp}°F, {wind} wind, {short_forecast}"

                if temp < 35 or wind_speed > 20:
                    boost *= 0.9
                if "Snow" in short_forecast or "Sleet" in short_forecast:
                    boost *= 0.85
                elif "Rain" in short_forecast or "Showers" in short_forecast:
                    boost *= 0.92
                break

        forecast_cache[key] = (round(boost, 3), condition)
        return forecast_cache[key]

    except Exception as e:
        print(f"❌ NOAA fetch error at lat={lat}, lon={lon}, using default boost. Reason: {e}")
        forecast_cache[key] = (1.0, "Unavailable")
        return forecast_cache[key]


def compute_weather_boost(stadium_profile, week, climate_phase, date):
    lat = stadium_profile.get("Latitude")
    lon = stadium_profile.get("Longitude")
    is_dome = stadium_profile.get("Dome", False)
    team = stadium_profile.get("Team", "")

    if is_dome:
        return 1.05, "Dome"

    if USE_FORECAST_WEATHER:
        return get_forecast_boost(lat, lon, date)

    return estimate_weather_boost(stadium_profile, week, climate_phase), "Climatology"


def build_weather_boost_map(schedule_df):
    env_df = load_csv(STADIUM_ENV_FILE)
    env_boost_map = {}

    for _, row in schedule_df.iterrows():
        week = row['Week']
        home_team = row['Home']
        date = row['Date']

        match = env_df[env_df['Team'] == home_team]
        if match.empty:
            boost, condition = 1.0, "Unknown"
        else:
            stadium_profile = match.iloc[0].to_dict()
            boost, condition = compute_weather_boost(stadium_profile, week, CLIMATE_PHASE, date)

        if week not in env_boost_map:
            env_boost_map[week] = {}
        env_boost_map[week][home_team] = {"boost": round(boost, 3), "condition": condition}

    return env_boost_map
