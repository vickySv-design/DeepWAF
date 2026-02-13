from flask import Blueprint, render_template
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/home')
def home():
    return render_template('home.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/model')
def model():
    return render_template('model.html')

@main_bp.route('/dashboard')
def dashboard():
    # Read logs
    log_file = 'logs/detections.log'
    total_requests = 0
    blocked_attacks = 0
    attack_types = {'signature': 0, 'CNN': 0}
    
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            for line in f:
                total_requests += 1
                if 'malicious' in line:
                    blocked_attacks += 1
                    if 'signature' in line:
                        attack_types['signature'] += 1
                    elif 'CNN' in line:
                        attack_types['CNN'] += 1
    
    return render_template('dashboard.html', 
                         total=total_requests,
                         blocked=blocked_attacks,
                         signature=attack_types['signature'],
                         cnn=attack_types['CNN'])
