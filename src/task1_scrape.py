import sys
import os
import re
import requests
from bs4 import BeautifulSoup
from typing import Dict

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


def fetch_wikipedia_page(url: str) -> str:
    """
    Fetch the HTML content of the given Wikipedia page.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def extract_title(soup: BeautifulSoup) -> str:
    """
    Extract the title of the Wikipedia page.
    """
    title_element = soup.find(id="firstHeading")
    if title_element:
        return title_element.get_text(strip=True)
    
    if soup.title:
        return soup.title.get_text(strip=True)
        
    return ""


def extract_first_sentence(soup: BeautifulSoup) -> str:
    """
    Extract the first sentence of the first paragraph on the Wikipedia page.
    """
    content = soup.find(id="mw-content-text") or soup
    paragraphs = content.find_all("p")
    
    for p in paragraphs:
        # separator=' ' гарантує, що слова з тегів <a> не злипнуться
        text = p.get_text(separator=' ', strip=True)
        # Очищаємо зайві пробіли
        text = ' '.join(text.split())
        
        if text and len(text) > 20:
            # Видаляємо номери посилань [1], [2] тощо
            clean_text = re.sub(r'\[\d+\]', '', text)
            
            # Розділяємо на речення по розділових знаках кінця речення
            sentences = re.split(r'(?<=[.!?])\s+', clean_text)
            if sentences:
                return sentences[0].strip()
                
    return ""


if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Web_scraping"
    try:
        page_content = fetch_wikipedia_page(url)
        soup = BeautifulSoup(page_content, 'html.parser')

        # Extract the title of the page
        title = extract_title(soup)

        # Extract the first sentence of the first paragraph
        first_sentence = extract_first_sentence(soup)

        # Combine the extracted data
        extracted_data = {
            "title": title,
            "first_sentence": first_sentence
        }

        # Print the extracted data
        print("Extracted Data:", extracted_data)

        # Save the data to a JSON file
        save_to_json(extracted_data, 'extracted_wikipedia_data.json')

        print("Data successfully saved to extracted_wikipedia_data.json")
    except Exception as e:
        print(f"An error occurred: {e}")