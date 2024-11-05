import requests
from bs4 import BeautifulSoup

def analyze_competitor_site(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        
        structure = []
        services = []
        
        # Extract links for site structure
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href.startswith('/'):
                structure.append(href)

        # Example: Extract services from specific HTML elements
        # Adjust the selector based on the actual structure of the competitor's site
        service_elements = soup.find_all(class_='service')  # Change 'service' to the actual class
        for service in service_elements:
            services.append(service.get_text(strip=True))
        
        return {
            'url': url,
            'structure': list(set(structure)),  # Remove duplicates
            'services': services
        }
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return {
            'url': url,
            'structure': [],
            'services': []
        }

def generate_recommendations(business_info, competitor_analysis):
    recommended_structure = []
    recommended_navbar = []

    # Example logic for generating recommendations based on competitor analysis
    for competitor in competitor_analysis:
        for service in competitor['services']:
            if service not in recommended_structure:
                recommended_structure.append(service)

    # Create a dynamic navbar based on the business's focus and competitors
    if business_info['industry'] == 'SEO':
        recommended_navbar = ['Home', 'Services', 'About Us', 'Contact']
        if 'link building' in business_info['skills'].lower():
            recommended_navbar.append('Link Building')
        if 'local seo' in business_info['skills'].lower():
            recommended_navbar.append('Local SEO')

    # Ensure the navbar contains unique items
    recommended_navbar = list(set(recommended_navbar))

    return recommended_structure, recommended_navbar