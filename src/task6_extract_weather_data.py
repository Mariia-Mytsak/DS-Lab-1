import csv
import os
import re
import sys
from typing import Any, Dict, List

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT_DIR = os.path.dirname(_CURRENT_DIR)
if _PARENT_DIR not in sys.path:
    sys.path.insert(0, _PARENT_DIR)
if _CURRENT_DIR not in sys.path:
    sys.path.insert(0, _CURRENT_DIR)

try:
    from src import utils
except ImportError:
    import utils


def clean_text(line: str) -> str:
    """
    Clean the text line by removing non-ASCII characters and fixing known issues.

    Args:
        line (str): The line of text to clean.

    Returns:
        str: The cleaned line of text.
    """
    cleaned = line.encode("ascii", "ignore").decode("ascii")
    cleaned = cleaned.replace("\xa0", " ").strip()
    return cleaned


def extract_weather_data(text_file: str) -> List[Dict[str, Any]]:
    """
    Extract weather data from a text file using regular expressions.

    Args:
        text_file (str): Path to the text file.

    Returns:
        list of dict: A list of dictionaries with extracted weather data.

    Raises:
        FileNotFoundError: If the text file does not exist.
    """
    extracted_data = []

    # Точний регулярний вираз для дати YYYY-MM-DD
    date_pattern = re.compile(r"Date:\s*(\d{4}-\d{2}-\d{2})", re.IGNORECASE)
    max_temp_pattern = re.compile(r"Max\s*Temp(?:erature)?:\s*(-?\d+(?:\.\d+)?)", re.IGNORECASE)
    min_temp_pattern = re.compile(r"Min\s*Temp(?:erature)?:\s*(-?\d+(?:\.\d+)?)", re.IGNORECASE)
    humidity_pattern = re.compile(r"Humidity:\s*(\d+(?:\.\d+)?)", re.IGNORECASE)
    precipitation_pattern = re.compile(r"Precipitation:\s*(\d+(?:\.\d+)?)", re.IGNORECASE)

    with open(text_file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    blocks = re.split(r"(?=Date:)", content, flags=re.IGNORECASE)

    for block in blocks:
        block_clean = clean_text(block)
        if not block_clean:
            continue

        date_match = date_pattern.search(block_clean)
        max_temp_match = max_temp_pattern.search(block_clean)
        min_temp_match = min_temp_pattern.search(block_clean)
        humidity_match = humidity_pattern.search(block_clean)
        precip_match = precipitation_pattern.search(block_clean)

        if date_match:
            date_val = date_match.group(1).strip()
            max_temp_val = float(max_temp_match.group(1)) if max_temp_match else 0.0
            min_temp_val = float(min_temp_match.group(1)) if min_temp_match else 0.0
            humidity_val = float(humidity_match.group(1)) if humidity_match else 0.0
            precip_val = float(precip_match.group(1)) if precip_match else 0.0

            extracted_data.append({
                "date": date_val,
                "max_temperature": max_temp_val,
                "min_temperature": min_temp_val,
                "humidity": humidity_val,
                "precipitation": precip_val
            })

    return extracted_data


def save_to_csv(data: List[Dict[str, Any]], filename: str = "extracted_weather_data.csv") -> None:
    """
    Save extracted weather data to a CSV file.

    Args:
        data (list of dict): Extracted weather data.
        filename (str): Name of the CSV file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    if not data:
        return

    header_map = {
        "date": "Date",
        "max_temperature": "Max Temperature",
        "min_temperature": "Min Temperature",
        "humidity": "Humidity",
        "precipitation": "Precipitation"
    }

    raw_keys = list(data[0].keys())
    fieldnames = [header_map.get(k, k) for k in raw_keys]

    with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            formatted_row = {header_map.get(k, k): v for k, v in row.items()}
            writer.writerow(formatted_row)


if __name__ == "__main__":
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        txt_path = os.path.join(script_dir, "weather_report.txt")
        if os.path.exists(txt_path):
            weather_data = extract_weather_data(txt_path)
            save_to_csv(weather_data)
            print("Data has been successfully extracted and saved to extracted_weather_data.csv.")
    except Exception as e:
        print(f"An error occurred: {e}")