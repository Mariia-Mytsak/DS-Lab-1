import csv
import os
import sys
import xml.etree.ElementTree as ET
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


def parse_weather_xml(xml_file: str) -> List[Dict[str, Any]]:
    """
    Parse weather data from an XML file.

    Args:
        xml_file (str): Path to the XML file.

    Returns:
        list of dict: A list of dictionaries with parsed weather data.

    Raises:
        FileNotFoundError: If the XML file does not exist.
        ET.ParseError: If the XML file is malformed.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    parsed_data = []

    nodes = root.findall(".//day") or root.findall(".//forecast") or root.findall(".//city") or list(root)

    for node in nodes:
        day_data = {}

        for attr, val in node.attrib.items():
            day_data[attr] = _convert_value(val)

        for child in node:
            tag = child.tag
            text = child.text.strip() if child.text else ""
            if text:
                day_data[tag] = _convert_value(text)
            for attr, val in child.attrib.items():
                day_data[f"{tag}_{attr}"] = _convert_value(val)

        if day_data:
            parsed_data.append(day_data)

    return parsed_data


def _convert_value(text: str) -> Any:
    """Вспомогательная функция для преобразования типов."""
    try:
        if "." in text:
            return float(text)
        return int(text)
    except ValueError:
        return text


def save_to_csv(data: List[Dict[str, Any]], filename: str = "parsed_weather_data.csv") -> None:
    """
    Save parsed weather data to a CSV file.
    """
    if not data:
        return

    header_map = {
        "date": "Date",
        "temperature": "Temperature",
        "temp": "Temperature",
        "humidity": "Humidity",
        "precipitation": "Precipitation",
        "precip": "Precipitation",
        "wind_speed": "Wind Speed",
        "weather_description": "Weather Description",
        "description": "Description"
    }

    raw_keys = list(data[0].keys())
    fieldnames = [header_map.get(k, k.capitalize() if k.islower() else k) for k in raw_keys]

    with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            formatted_row = {}
            for k, v in row.items():
                new_key = header_map.get(k, k.capitalize() if k.islower() else k)
                formatted_row[new_key] = v
            writer.writerow(formatted_row)


if __name__ == "__main__":
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        xml_path = os.path.join(script_dir, "weather_data.xml")

        if os.path.exists(xml_path):
            weather_data = parse_weather_xml(xml_path)
            save_to_csv(weather_data, "parsed_weather_data.csv")
            print("Data has been successfully parsed and saved to parsed_weather_data.csv.")
    except Exception as e:
        print(f"An error occurred: {e}")