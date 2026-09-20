import sys
import os
from typing import Dict, List, Any

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import load_json


def analyze_daily_weather(day: Dict[str, Any], temp_threshold: float = 30, 
                           wind_threshold: float = 15, humidity_threshold: float = 70) -> Dict[str, Any]:
    """
    Analyze weather data for a single day.
    """
    date = day.get("date", "")
    hourly = day.get("hourly", {})
    
    temps = hourly.get("temperature", [])
    winds = hourly.get("wind_speed", [])
    humidities = hourly.get("humidity", [])

    avg_temp = sum(temps) / len(temps) if temps else 0.0
    max_temp = max(temps) if temps else 0.0
    avg_wind = sum(winds) / len(winds) if winds else 0.0
    avg_humidity = sum(humidities) / len(humidities) if humidities else 0.0

    is_hot = max_temp > temp_threshold
    is_windy = avg_wind > wind_threshold
    is_uncomfortable = avg_temp > temp_threshold and avg_humidity > humidity_threshold

    return {
        "date": date,
        "avg_temp": avg_temp,
        "max_temp": max_temp,
        "avg_wind": avg_wind,
        "avg_humidity": avg_humidity,
        "is_hot": is_hot,
        "is_windy": is_windy,
        "is_uncomfortable": is_uncomfortable
    }


def generate_daily_report(analysis: Dict[str, Any]) -> str:
    """
    Generate a detailed report based on the analysis results for a single day.
    """
    date = analysis.get("date", "Unknown")
    avg_temp = analysis.get("avg_temp", 0.0)
    max_temp = analysis.get("max_temp", 0.0)
    avg_wind = analysis.get("avg_wind", 0.0)
    avg_humidity = analysis.get("avg_humidity", 0.0)

    report = (
        f"Date: {date}\n"
        f"Average Temperature: {avg_temp:.2f}°C\n"
        f"Max Temperature: {max_temp:.2f}°C\n"
        f"Average Wind Speed: {avg_wind:.2f} km/h\n"
        f"Average Humidity: {avg_humidity:.2f}%\n"
        f"Hot Day: {'Yes' if analysis.get('is_hot') else 'No'}\n"
        f"Windy Day: {'Yes' if analysis.get('is_windy') else 'No'}\n"
        f"Uncomfortable Day: {'Yes' if analysis.get('is_uncomfortable') else 'No'}"
    )
    return report


def summarize_weather_analysis(analyses: List[Dict[str, Any]]) -> str:
    """
    Summarize the weather analysis over multiple days.
    """
    total_days = len(analyses)
    if total_days == 0:
        return "No weather data available."

    hot_days = sum(1 for a in analyses if a.get("is_hot"))
    windy_days = sum(1 for a in analyses if a.get("is_windy"))
    uncomfortable_days = sum(1 for a in analyses if a.get("is_uncomfortable"))
    max_temp_overall = max((a.get("max_temp", 0.0) for a in analyses), default=0.0)

    summary = (
        f"Weather Analysis Summary:\n"
        f"Total Days Analyzed: {total_days}\n"
        f"Hot Days: {hot_days}\n"
        f"Windy Days: {windy_days}\n"
        f"Uncomfortable Days: {uncomfortable_days}\n"
        f"Highest Recorded Temperature: {max_temp_overall:.2f}°C"
    )
    return summary


if __name__ == "__main__":
    try:
        # Load the JSON data
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "tokyo_weather_complex.json")
        weather_data = load_json(json_path)

        # Analyze the weather data for each day
        analyses = [analyze_daily_weather(day) for day in weather_data['daily']]

        # Generate and print daily reports
        for analysis in analyses:
            report = generate_daily_report(analysis)
            print(report)

        # Generate and print a summary report
        summary_report = summarize_weather_analysis(analyses)
        print(summary_report)
    except Exception as e:
        print(f"An error occurred: {e}")