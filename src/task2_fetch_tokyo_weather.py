import requests
import sys
import os

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

def fetch_weather_data() -> Dict[str, any]:
    """
    Fetch the maximum temperature forecast for Tokyo using the Open-Meteo API.

    Returns:
        dict: A dictionary containing the date and the maximum temperature.

    Raises:
        requests.HTTPError: If the HTTP request returned an unsuccessful status code.
        requests.RequestException: If there was a network error.
        KeyError: If the expected data is not in the API response.
    """
    url = ("https://api.open-meteo.com/v1/forecast?latitude=35.6895&longitude=139.6917"
           "&daily=temperature_2m_max&timezone=Asia/Tokyo")
    
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Отримуємо масиви дат та температур з відповіді API
    dates = data["daily"]["time"]
    max_temperatures = data["daily"]["temperature_2m_max"]

    return {
        "date": dates,
        "max_temperature": max_temperatures
    }


if __name__ == "__main__":
    try:
        # Fetch the weather data
        weather_data = fetch_weather_data()

        # Save the data to a JSON file
        save_to_json(weather_data, "tokyo_weather.json")

        print("Data successfully saved to tokyo_weather.json")
    except Exception as e:
        print(f"An error occurred: {e}")