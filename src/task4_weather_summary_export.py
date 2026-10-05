import csv
import sys
import os
from typing import Dict, List, Union, TextIO, Any

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT_DIR = os.path.dirname(_CURRENT_DIR)
if _PARENT_DIR not in sys.path:
    sys.path.insert(0, _PARENT_DIR)
if _CURRENT_DIR not in sys.path:
    sys.path.insert(0, _CURRENT_DIR)

try:
    from src.utils import load_json, save_to_json
except ImportError:
    from utils import load_json, save_to_json

def summarize_weather_data(data: List[Dict[str, Any]]) -> Dict[str, Union[float, int]]:
    """
    Summarize the weather data across all days.
    """
    if not data:
        return {
            "average_max_temp": 0.0,
            "average_min_temp": 0.0,
            "total_precipitation": 0.0,
            "average_wind_speed": 0.0,
            "average_humidity": 0.0,
            "hot_days": 0,
            "windy_days": 0,
            "rainy_days": 0
        }

    max_temps = []
    min_temps = []
    precipitations = []
    wind_speeds = []
    humidities = []
    hot_days = 0
    windy_days = 0
    rainy_days = 0

    for day in data:
        max_t = day.get("max_temp", day.get("max_temperature", 0.0))
        min_t = day.get("min_temp", day.get("min_temperature", 0.0))
        precip = day.get("precipitation", 0.0)
        wind_s = day.get("max_wind_speed", day.get("wind_speed", 0.0))
        humid = day.get("avg_humidity", day.get("humidity", 0.0))

        max_temps.append(max_t)
        min_temps.append(min_t)
        precipitations.append(precip)
        wind_speeds.append(wind_s)
        humidities.append(humid)

        if day.get("is_hot_day", max_t > 30):
            hot_days += 1
        if day.get("is_windy_day", wind_s > 15):
            windy_days += 1
        if day.get("is_rainy_day", precip > 0):
            rainy_days += 1

    return {
        "average_max_temp": sum(max_temps) / len(max_temps) if max_temps else 0.0,
        "average_min_temp": sum(min_temps) / len(min_temps) if min_temps else 0.0,
        "total_precipitation": sum(precipitations),
        "average_wind_speed": sum(wind_speeds) / len(wind_speeds) if wind_speeds else 0.0,
        "average_humidity": sum(humidities) / len(humidities) if humidities else 0.0,
        "hot_days": hot_days,
        "windy_days": windy_days,
        "rainy_days": rainy_days
    }


def export_to_csv(data: List[Dict[str, Any]], file: Union[str, TextIO]) -> None:
    """
    Export the summarized weather data to a CSV file or file-like object.
    """
    headers = [
        "Date",
        "Max Temperature",
        "Min Temperature",
        "Precipitation",
        "Wind Speed",
        "Humidity",
        "Weather Description",
        "Is Hot Day",
        "Is Windy Day",
        "Is Rainy Day",
    ]

    def write_data(writer: csv.DictWriter) -> None:
        """Helper function to write rows to the CSV."""
        writer.writeheader()
        for day in data:
            max_t = day.get("max_temp", day.get("max_temperature", 0.0))
            wind_s = day.get("max_wind_speed", day.get("wind_speed", 0.0))
            precip = day.get("precipitation", 0.0)

            writer.writerow({
                "Date": day.get("date", ""),
                "Max Temperature": max_t,
                "Min Temperature": day.get("min_temp", day.get("min_temperature", 0.0)),
                "Precipitation": precip,
                "Wind Speed": wind_s,
                "Humidity": day.get("avg_humidity", day.get("humidity", 0.0)),
                "Weather Description": day.get("weather_description", day.get("description", "")),
                "Is Hot Day": day.get("is_hot_day", max_t > 30),
                "Is Windy Day": day.get("is_windy_day", wind_s > 15),
                "Is Rainy Day": day.get("is_rainy_day", precip > 0)
            })

    if isinstance(file, str):
        with open(file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            write_data(writer)
    else:
        writer = csv.DictWriter(file, fieldnames=headers)
        write_data(writer)


if __name__ == "__main__":
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "tokyo_weather_complex.json")

        if os.path.exists(json_path):
            weather_data = load_json(json_path)
            daily_data = weather_data.get("daily", []) if isinstance(weather_data, dict) else weather_data

            summary = summarize_weather_data(daily_data)

            print("Weather Data Summary:")
            for key, value in summary.items():
                print(f"{key}: {value}")

            export_to_csv(daily_data, "tokyo_weather_summary.csv")
            print("Data successfully exported to tokyo_weather_summary.csv")
    except Exception as e:
        print(f"An error occurred: {e}")