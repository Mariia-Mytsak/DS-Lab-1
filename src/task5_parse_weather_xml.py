import os
import sys
import xml.etree.ElementTree as ET
from typing import Dict, List, Any

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PARENT_DIR = os.path.dirname(_CURRENT_DIR)
if _CURRENT_DIR not in sys.path:
    sys.path.insert(0, _CURRENT_DIR)
if _PARENT_DIR not in sys.path:
    sys.path.insert(0, _PARENT_DIR)

try:
    import utils
except ImportError:
    from src import utils


def parse_weather_xml(xml_file: str) -> List[Dict[str, any]]:
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

    # Проходимо по кожному елементу дня/запису в XML
    for day in root.findall(".//day") or root.findall(".//city") or root:
        # Перевіряємо, чи є підтеги дня, якщо це список днів
        day_data = {}
        for child in day:
            tag = child.tag
            text = child.text.strip() if child.text else ""
            
            # Конвертуємо числові значення за наявності
            try:
                if "." in text:
                    value = float(text)
                else:
                    value = int(text)
            except ValueError:
                value = text
                
            day_data[tag] = value
            
        if day_data:
            parsed_data.append(day_data)

    # Якщо структура XML інша (наприклад, суцільні атрибути чи тег forecast)
    if not parsed_data:
        for item in root.iter():
            if item.attrib:
                parsed_data.append(item.attrib)

    return parsed_data


def save_to_csv(data: List[Dict[str, any]], filename: str = "parsed_weather_data.csv") -> None:
    """
    Save parsed weather data to a CSV file.

    Args:
        data (list of dict): Parsed weather data.
        filename (str): Name of the CSV file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    if not data:
        return

    # Визначаємо всі можливі ключі для заголовків CSV
    fieldnames = list(data[0].keys())

    with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    try:
        # Parse the XML file
        import os
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        xml_path = os.path.join(script_dir, "weather_data.xml")
        weather_data = parse_weather_xml(xml_path)

        # Save the parsed data to a CSV file
        save_to_csv(weather_data)
        print("Data has been successfully parsed and saved to parsed_weather_data.csv.")
    except Exception as e:
        print(f"An error occurred: {e}")