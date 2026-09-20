import csv
import sys
import os
from typing import Dict, List, Union, TextIO

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import load_json


def summarize_weather_data(data: List[Dict[str, any]]) -> Dict[str, float]:
    """
    Summarize the weather data across all days.

    Args:
        data (list of dict): The daily weather data.

    Returns:
        dict: A summary of the key metrics across all days.
    """
    if not data:
        return {
            "avg_max_temp": 0.0,
            "avg_min_temp": 0.0,
            "total_precipitation": 0.0,
            "max_wind_speed": 0.0,
            "avg_humidity": 0.0
        }

    max_temps = []
    min_temps = []
    precipitations = []
    wind_speeds = []
    humidities = []

    for day in data:
        max_temps.append(day.get("max_temp", 0.0))
        min_temps.append(day.get("min_temp", 0.0))
        precipitations.append(day.get("precipitation", 0.0))
        wind_speeds.append(day.get("max_wind_speed", day.get("wind_speed", 0.0)))
        humidities.append(day.get("avg_humidity", day.get("humidity", 0.0)))

    return {
        "avg_max_temp": sum(max_temps) / len(max_temps) if max_temps else 0.0,
        "avg_min_temp": sum(min_temps) / len(min_temps) if min_temps else 0.0,
        "total_precipitation": sum(precipitations),
        "max_wind_speed": max(wind_speeds) if wind_speeds else 0.0,
        "avg_humidity": sum(humidities) / len(humidities) if humidities else 0.0
    }


def export_to_csv(data: List[Dict[str, any]], file: Union[str, TextIO]) -> None:
    """
    Export the summarized weather data to a CSV file or file-like object.

    Args:
        data (list of dict): The daily weather data to export.
        file (str or file-like object): The name of the CSV file to save the data in, or a file-like object.
    """
    headers = ["Date", "Max Temperature", "Min Temperature", "Precipitation", "Wind Speed", "Humidity",
               "Weather Description", "Is Hot Day", "Is Windy Day", "Is Rainy Day"]

    def write_data(writer: csv.DictWriter) -> None:
        """Helper function to write rows to the CSV."""
        writer.writeheader()
        for day in data:
            max_t = day.get("max_temp", 0.0)
            wind_s = day.get("max_wind_speed", day.get("wind_speed", 0.0))
            precip = day.get("precipitation", 0.0)

            writer.writerow({
                "Date": day.get("date", ""),
                "Max Temperature": max_t,
                "Min Temperature": day.get("min_temp", 0.0),
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
        # Load the JSON data
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "tokyo_weather_complex.json")
        weather_data = load_json(json_path)

        # Summarize the weather data
        summary = summarize_weather_data(weather_data['daily'])

        # Print the summary for verification
        print("Weather Data Summary:")
        for key, value in summary.items():
            print(f"{key}: {value}")

        # Export the summarized data to a CSV file
        export_to_csv(weather_data['daily'], "tokyo_weather_summary.csv")

        print("Data successfully exported to tokyo_weather_summary.csv")
    except Exception as e:
        print(f"An error occurred: {e}")