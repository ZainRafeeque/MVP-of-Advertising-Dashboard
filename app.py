from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import random
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY') or os.urandom(24)

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# AI Configuration
app.config['AI_API_KEY'] = os.getenv('AI_API_KEY')
app.config['AI_ENDPOINT'] = 'https://api.openai.com/v1/chat/completions'

# Flask Login Setup
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Mock User System
class User(UserMixin):
    def __init__(self, user_id, email, name):
        self.id = user_id
        self.email = email
        self.name = name

users = {'1': User('1', 'admin@example.com', 'Admin User')}

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

# Mock Campaign Database
campaigns_db = []
INTERESTS = ['Technology', 'Fashion', 'Sports', 'Travel', 'Food', 'Health']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        if email == 'admin@example.com':
            user = users.get('1')
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials. Try admin@example.com', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', 
                         user=current_user,
                         campaigns=campaigns_db)

@app.route('/campaigns/create', methods=['GET', 'POST'])
@login_required
def create_campaign():
    if request.method == 'POST':
        campaign_name = request.form.get('name', '').strip()
        age_range = request.form.get('age_range', '25-45')
        location = request.form.get('location', 'US')
        interests = request.form.getlist('interests') or ['General']
        banner_url = request.form.get('banner_url', '').strip()

        # Handle file upload
        if 'banner' in request.files:
            file = request.files['banner']
            if file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                banner_url = url_for('uploaded_file', filename=filename, _external=True)

        # Generate AI ad copy
        ai_ad_copy = generate_ai_ad_copy(campaign_name, ', '.join(interests))
        
        # Simulate analytics
        impressions = random.randint(1000, 10000)
        ctr = round(random.uniform(0.5, 5.0), 2)

        new_campaign = {
            'id': len(campaigns_db) + 1,
            'name': campaign_name,
            'ad_copy': ai_ad_copy,
            'banner': banner_url or "https://via.placeholder.com/120?text=No+Image",
            'date': datetime.now().strftime("%Y-%m-%d"),
            'status': 'Active',
            'impressions': impressions,
            'ctr': ctr,
            'targeting': {
                'age': age_range,
                'location': location,
                'interests': interests
            }
        }

        campaigns_db.append(new_campaign)
        flash(f'Campaign "{campaign_name}" created successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('create_campaign.html', interests=INTERESTS)

@app.route('/campaigns/<int:campaign_id>')
@login_required
def view_campaign(campaign_id):
    campaign = next((c for c in campaigns_db if c['id'] == campaign_id), None)
    if not campaign:
        flash('Campaign not found', 'danger')
        return redirect(url_for('dashboard'))
    return render_template('view_campaign.html', campaign=campaign)

def generate_ai_ad_copy(product_name, keywords):
    """Generate ad copy using AI"""
    if not app.config['AI_API_KEY']:
        return f"Engaging ad copy for {product_name} targeting {keywords}."
    
    try:
        headers = {
            "Authorization": f"Bearer {app.config['AI_API_KEY']}",
            "Content-Type": "application/json"
        }
        prompt = f"Create a 1-2 sentence engaging ad for {product_name} targeting {keywords}."
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        response = requests.post(app.config['AI_ENDPOINT'], headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"AI Error: {e}")
        return f"Engaging ad for {product_name} - {keywords}"

if __name__ == '__main__':
    app.run(debug=True) 