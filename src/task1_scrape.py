import requests
from bs4 import BeautifulSoup
from typing import Dict

try:
    from .utils import save_to_json
except ImportError:
    from utils import save_to_json


def fetch_wikipedia_page(url: str) -> str:
    """
    Fetch the HTML content of the given Wikipedia page.
    """
    response = requests.get(url)
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
    # Знаходимо всі параграфи в основному вмісті статті
    paragraphs = soup.select("p")
    
    for p in paragraphs:
        text = p.get_text(strip=True)
        # Пропускаємо порожні параграфи
        if text:
            # Розділяємо параграф на речення по першій крапці
            sentences = text.split('.')
            if sentences:
                return sentences[0].strip() + '.'
                
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