import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_keyword_data(keyword):
    # Replace 'example.com' with the URL you want to scrape
    url = f'https://www.example.com/search?q={keyword}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This will depend on the structure of the page you're scraping
        # Look for elements that contain search volume data
        search_volume = soup.find('div', class_='volume')  # Adjust according to actual HTML structure
        
        return search_volume.text if search_volume else 'Data not found'
    else:
        return 'Failed to retrieve data'

if __name__ == '__main__':
    keyword = input("Enter a keyword to search: ")
    volume = scrape_keyword_data(keyword)
    print(f'Search volume for "{keyword}": {volume}')
