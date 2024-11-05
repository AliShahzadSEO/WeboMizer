import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re

def categorize_url(url):
    """Categorize URLs into meaningful sections"""
    service_patterns = {
        'content': r'content|blog|articles',
        'seo': r'seo|search-engine|keywords',
        'web-design': r'design|ui|ux|layout',
        'analytics': r'analytics|tracking|metrics|data',
        'marketing': r'marketing|advertising|promotion',
        'about': r'about|company|team|values',
        'contact': r'contact|support|help',
        'portfolio': r'portfolio|work|projects|case-studies'
    }
    
    url_lower = url.lower()
    for category, pattern in service_patterns.items():
        if re.search(pattern, url_lower):
            return category
    return 'other'

def analyze_competitor_site(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Initialize structure dictionary
        structure = defaultdict(list)
        
        # Analyze navigation
        nav_elements = soup.find_all(['nav', 'header'])
        for nav in nav_elements:
            links = nav.find_all('a')
            for link in links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                if href and href.startswith('/'):
                    category = categorize_url(href)
                    structure[category].append({
                        'url': href,
                        'text': text
                    })
        
        # Analyze main content
        content_elements = soup.find_all(['main', 'article', 'section'])
        services = []
        for element in content_elements:
            service_headings = element.find_all(['h1', 'h2', 'h3'])
            for heading in service_headings:
                services.append(heading.get_text(strip=True))
        
        return {
            'url': url,
            'structure': dict(structure),
            'services': list(set(services))
        }
    except Exception as e:
        print(f"Error analyzing {url}: {str(e)}")
        return {
            'url': url,
            'structure': {},
            'services': []
        }

def generate_recommendations(business_info, competitor_analysis):
    """Generate improved recommendations based on business info and competitor analysis"""
    
    # Initialize recommendations
    recommended_structure = {
        'main_sections': [],
        'services': [],
        'content_types': [],
        'conversion_points': []
    }
    
    # Basic sections every site should have
    basic_sections = ['Home', 'About', 'Services', 'Contact']
    recommended_structure['main_sections'].extend(basic_sections)
    
    # Analyze business info for customized recommendations
    if business_info.get('industry'):
        recommended_structure['services'].append(f"{business_info['industry']} Services")
    
    if business_info.get('skills'):
        skills = [skill.strip() for skill in business_info['skills'].split(',')]
        recommended_structure['services'].extend(skills)
    
    # Add content types based on target audience
    if business_info.get('target_audience'):
        recommended_structure['content_types'].extend([
            'Case Studies',
            'Industry Resources',
            'Blog',
            'Knowledge Base'
        ])
    
    # Analyze competitor structures
    common_sections = defaultdict(int)
    for competitor in competitor_analysis:
        for category, items in competitor.get('structure', {}).items():
            common_sections[category] += 1
    
    # Add popular competitor sections
    for category, count in common_sections.items():
        if count >= len(competitor_analysis) / 2:  # If section appears in at least half of competitor sites
            if category not in recommended_structure['main_sections']:
                recommended_structure['main_sections'].append(category.title())
    
    # Generate navbar recommendations
    recommended_navbar = []
    
    # Primary navigation
    primary_nav = ['Home', 'Services', 'About']
    if 'Portfolio' in recommended_structure['main_sections']:
        primary_nav.append('Portfolio')
    primary_nav.extend(['Blog', 'Contact'])
    
    # Service dropdown items
    service_dropdown = []
    for service in recommended_structure['services'][:5]:  # Limit to top 5 services
        service_dropdown.append(service)
    
    return recommended_structure, {
        'primary_nav': primary_nav,
        'service_dropdown': service_dropdown
    }

def format_recommendations(recommended_structure, navbar):
    """Format recommendations into a presentable structure"""
    formatted_output = {
        'Main Navigation': navbar['primary_nav'],
        'Services Menu': navbar['service_dropdown'],
        'Recommended Pages': {
            'Main Sections': recommended_structure['main_sections'],
            'Service Pages': recommended_structure['services'],
            'Content Types': recommended_structure['content_types']
        },
        'Conversion Points': [
            'Free Consultation',
            'Contact Form',
            'Service Quote Calculator',
            'Newsletter Signup',
            'Download Resources'
        ]
    }
    return formatted_output