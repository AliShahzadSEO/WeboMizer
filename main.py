from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from scraper import scrape_keyword_data  # Import the scraping function
from predict import predict_service_category
from train_model import train_test_split

app = Flask(__name__)
app.secret_key = '94751c46ad63108d32348baa2ae4d9e2'  # Required for session management

# Load the services database
services_data = pd.read_csv(r'Data/services_database.csv')

# Strip leading/trailing spaces from column names
services_data.columns = services_data.columns.str.strip()

@app.route('/get_categories', methods=['POST'])
def get_categories():
    selected_project_type = request.form['project_type']
    categories = services_data[services_data['Project Type'] == selected_project_type]['Main Category'].unique()
    return {'categories': list(categories)}

@app.route('/get_subcategories', methods=['POST'])
def get_subcategories():
    selected_category = request.form['category']
    subcategories = services_data[services_data['Main Category'] == selected_category]['Subcategory'].unique()
    return {'subcategories': list(subcategories)}

@app.route('/get_services', methods=['POST'])
def get_services():
    selected_subcategory = request.form['subcategory']
    services = services_data[services_data['Subcategory'] == selected_subcategory]['Service'].unique()
    return {'services': list(services)}

@app.route('/get_sub_services', methods=['POST'])
def get_sub_services():
    selected_service = request.form['service']
    sub_services = services_data[services_data['Service'] == selected_service]['Sub-service'].unique()
    return {'sub_services': list(sub_services)}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/project_details', methods=['POST'])
def project_details():
    # Capture project details from form
    project_info = {
        'business_name': request.form['business_name'],
        'business_url': request.form['business_url'],
        'business_description': request.form['business_description'],
        'keywords': request.form['keywords'],
    }
    # Store project_info in session
    session['project_info'] = project_info
    return render_template('competitors.html')

@app.route('/competitors', methods=['POST'])
def competitors():
    # Get competitors' URLs
    competitor_urls = request.form['competitor_urls'].split(',')
    # Store competitor URLs in session
    session['competitor_urls'] = competitor_urls
    return redirect(url_for('result'))

@app.route('/result', methods=['GET'])
def result():
    # Retrieve project info and competitor URLs from session
    project_info = session.get('project_info', {})
    competitor_urls = session.get('competitor_urls', [])

    # Use the keyword(s) from project_info to scrape data
    keywords = project_info.get('keywords', '').split(',')
    search_volumes = {}

    for keyword in keywords:
        search_volume = scrape_keyword_data(keyword.strip())  # Strip any whitespace
        search_volumes[keyword] = search_volume

    # Pass data to the result template
    return render_template('result.html', project_info=project_info, competitor_urls=competitor_urls, search_volumes=search_volumes)

if __name__ == '__main__':
    app.run(debug=True)
