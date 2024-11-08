from flask import Flask, render_template, request, redirect, url_for, session
from site_analyzer import analyze_competitor_site, generate_recommendations, format_recommendations

app = Flask(__name__)
app.secret_key = '94751c46ad63108d32348baa2ae4d9e2'  # Required for session management

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/project_details', methods=['POST'])
def project_details():
    business_info = {
        'business_name': request.form['business_name'],
        'business_url': request.form['business_url'],
        'business_description': request.form['business_description'],
        'keywords': request.form['keywords'],
        'industry': request.form['industry'],
        'sub_industry': request.form['sub_industry'],
        'main_services': request.form['main_services'],
        'sub_services': request.form['sub_services'],
        'solutions': request.form['solutions'],
        'skills': request.form['skills'],
        'target_audience': request.form['target_audience'],
        'service_goals': request.form['service_goals'],
    }
    session['business_info'] = business_info
    return render_template('competitors.html')

@app.route('/competitors', methods=['GET', 'POST'])
def competitors():
    if request.method == 'POST':
        competitor_urls = request.form.get('competitor_urls', '').split(',')
        session['competitor_urls'] = competitor_urls
        return redirect(url_for('site_architecture'))
    return render_template('competitors.html')

@app.route('/site_architecture')
def site_architecture():
    business_info = session.get('business_info', {})
    competitor_urls = session.get('competitor_urls', [])
    
    competitor_analysis = []
    for url in competitor_urls:
        analysis = analyze_competitor_site(url.strip())
        competitor_analysis.append(analysis)
    
    recommended_structure, navbar = generate_recommendations(business_info, competitor_analysis)
    formatted_recommendations = format_recommendations(recommended_structure, navbar)
    
    return render_template('site_architecture.html',
                         business_info=business_info,
                         competitor_analysis=competitor_analysis,
                         recommendations=formatted_recommendations)

if __name__ == '__main__':
    app.run(debug=True)