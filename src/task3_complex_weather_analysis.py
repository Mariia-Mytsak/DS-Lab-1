import sys
import os
from typing import Dict, Any, List

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT_DIR = os.path.dirname(_CURRENT_DIR)
if _PARENT_DIR not in sys.path:
    sys.path.insert(0, _PARENT_DIR)
if _CURRENT_DIR not in sys.path:
    sys.path.insert(0, _CURRENT_DIR)

try:
    from src.utils import save_to_json, load_json
except ImportError:
    from utils import save_to_json, load_json


def analyze_daily_weather(day: Dict[str, Any], temp_threshold: float = 30, 
                           wind_threshold: float = 15, humidity_threshold: float = 70) -> Dict[str, Any]:
    """
    Analyze weather data for a single day.
    """
    date = day.get("date", "")
    max_temp = day.get("max_temperature", 0.0)
    min_temp = day.get("min_temperature", 0.0)
    wind_speed = day.get("wind_speed", 0.0)
    humidity = day.get("humidity", 0.0)
    precipitation = day.get("precipitation", 0.0)
    weather_description = day.get("weather_description", "")

    temp_swing = max_temp - min_temp
    is_hot_day = max_temp > temp_threshold
    is_windy_day = wind_speed > wind_threshold
    is_uncomfortable_day = (max_temp > temp_threshold) and (humidity > humidity_threshold)
    is_rainy_day = precipitation > 0.0

    return {
        "date": date,
        "max_temperature": max_temp,
        "min_temperature": min_temp,
        "temperature_swing": temp_swing,
        "wind_speed": wind_speed,
        "humidity": humidity,
        "precipitation": precipitation,
        "weather_description": weather_description,
        "is_hot_day": is_hot_day,
        "is_windy_day": is_windy_day,
        "is_uncomfortable_day": is_uncomfortable_day,
        "is_rainy_day": is_rainy_day
    }


def generate_daily_report(analysis: Dict[str, Any]) -> str:
    """
    Generate a detailed report based on the analysis results for a single day.
    """
    date = analysis.get("date", "Unknown")
    max_temp = analysis.get("max_temperature", 0.0)
    min_temp = analysis.get("min_temperature", 0.0)
    avg_temp = (max_temp + min_temp) / 2.0
    wind_speed = analysis.get("wind_speed", 0.0)
    humidity = analysis.get("humidity", 0.0)
    desc = analysis.get("weather_description", "")
    precip = analysis.get("precipitation", 0.0)

    is_hot = "Yes" if analysis.get("is_hot_day") else "No"
    is_windy = "Yes" if analysis.get("is_windy_day") else "No"
    is_uncomfortable = "Yes" if analysis.get("is_uncomfortable_day") else "No"

    max_str = f"{max_temp:g}" if isinstance(max_temp, float) else str(max_temp)
    min_str = f"{min_temp:g}" if isinstance(min_temp, float) else str(min_str)
    
    precip_str = f"{precip:g} mm precipitation" if precip > 0 else "no precipitation"

    report = (
        f"Date: {date}\n"
        f"weather: {desc}\n"
        f"Average Temperature: {avg_temp:.2f}°C\n"
        f"Max {max_str}°C, Min {min_str}°C\n"
        f"Average Wind Speed: {wind_speed:.2f} km/h\n"
        f"Average Humidity: {humidity:.0f}%\n"
        f"Precipitation: {precip_str}\n"
        f"hot day: {is_hot}\n"
        f"windy day: {is_windy}\n"
        f"uncomfortable day: {is_uncomfortable}"
    )
    return report


def summarize_weather_analysis(analyses: List[Dict[str, Any]]) -> str:
    """
    Summarize the weather analysis over multiple days.
    """
    total_days = len(analyses)
    if total_days == 0:
        return "No weather data available."

    hot_days = sum(1 for a in analyses if a.get("is_hot_day"))
    windy_days = sum(1 for a in analyses if a.get("is_windy_day"))
    uncomfortable_days = sum(1 for a in analyses if a.get("is_uncomfortable_day"))
    
    hottest_day_entry = max(analyses, key=lambda a: a.get("max_temperature", -999.0))
    hottest_date = hottest_day_entry.get("date", "")
    max_temp_overall = hottest_day_entry.get("max_temperature", 0.0)

    windiest_day_entry = max(analyses, key=lambda a: a.get("wind_speed", -999.0))
    windiest_date = windiest_day_entry.get("date", "")
    max_wind_overall = windiest_day_entry.get("wind_speed", 0.0)

    most_humid_entry = max(analyses, key=lambda a: a.get("humidity", -999.0))
    most_humid_date = most_humid_entry.get("date", "")
    max_humidity_overall = most_humid_entry.get("humidity", 0.0)

    rainiest_day_entry = max(analyses, key=lambda a: a.get("precipitation", -999.0))
    rainiest_date = rainiest_day_entry.get("date", "")
    max_precip_overall = rainiest_day_entry.get("precipitation", 0.0)

    temp_str = f"{max_temp_overall:g}" if isinstance(max_temp_overall, float) else str(max_temp_overall)
    wind_str = f"{max_wind_overall:.1f}" if isinstance(max_wind_overall, float) else str(max_wind_overall)
    humid_str = f"{max_humidity_overall:.0f}" if isinstance(max_humidity_overall, float) else str(max_humidity_overall)
    precip_str = f"{max_precip_overall:.1f}" if isinstance(max_precip_overall, float) else str(max_precip_overall)

    summary = (
        f"Weather Analysis Summary:\n"
        f"Total Days Analyzed: {total_days}\n"
        f"Hot Days: {hot_days}\n"
        f"Windy Days: {windy_days}\n"
        f"Uncomfortable Days: {uncomfortable_days}\n"
        f"Hottest day: {hottest_date}\n"
        f"Windiest day: {windiest_date}\n"
        f"Most humid day: {most_humid_date}\n"
        f"Rainiest day: {rainiest_date}\n"
        f"Highest Humidity: {humid_str}%\n"
        f"Highest Wind Speed: {wind_str} km/h\n"
        f"Highest Recorded Temperature: {temp_str}°C\n"
        f"Highest Precipitation: {precip_str} mm"
    )
    return summary


if __name__ == "__main__":
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "tokyo_weather_complex.json")
        if os.path.exists(json_path):
            weather_data = load_json(json_path)
            daily_list = weather_data.get("daily", []) if isinstance(weather_data, dict) else weather_data
            analyses = [analyze_daily_weather(day) for day in daily_list]

            for analysis in analyses:
                print(generate_daily_report(analysis))

            print(summarize_weather_analysis(analyses))
    except Exception as e:
        print(f"An error occurred: {e}")