from flask import Flask, render_template, request, redirect, url_for, session
from site_analyzer import analyze_competitor_site, generate_recommendations

app = Flask(__name__)
app.secret_key = '94751c46ad63108d32348baa2ae4d9e2'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/competitors', methods=['POST'])
def competitors():
    business_info = {
        'business_name': request.form['business_name'],
        'business_url': request.form['business_url'],
        'business_description': request.form['business_description'],
        'keywords': request.form['keywords'],
    }
    session['business_info'] = business_info
    return render_template('competitors.html')

@app.route('/site_architecture', methods=['POST'])
def site_architecture():
    business_info = session.get('business_info', {})
    competitor_urls = request.form['competitor_urls'].split(',')
    
    competitor_analysis = []
    for url in competitor_urls:
        analysis = analyze_competitor_site(url.strip())
        competitor_analysis.append(analysis)
    
    recommended_structure, recommended_navbar = generate_recommendations(business_info, competitor_analysis)
    
    return render_template('site_architecture.html',
                           business_info=business_info,
                           competitor_analysis=competitor_analysis,
                           recommended_structure=recommended_structure,
                           recommended_navbar=recommended_navbar)

if __name__ == '__main__':
    app.run(debug=True)