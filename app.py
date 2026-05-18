from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager
from backend.models import db, User
from config import Config
import os
from datetime import timedelta

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    app.config['SESSION_PERMANENT'] = True

    # Initialize extensions
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create upload folder
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Register Blueprints
    from backend.routes.auth import auth_bp
    from backend.routes.admin import admin_bp
    from backend.routes.staff import staff_bp
    from backend.routes.notifications import notify_bp
    from backend.routes.help import help_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(notify_bp)
    app.register_blueprint(help_bp)

    @app.context_processor
    def inject_unread_count():
        from flask_login import current_user
        if current_user.is_authenticated:
            from backend.models import Notification
            count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
            return {'unread_notif_count': count}
        return {'unread_notif_count': 0}

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Initialize Risk Rules if they don't exist
        from backend.models import RiskRule
        default_rules = [
            ('gpa_high_threshold', 2.0, 'GPA below this is considered High Risk'),
            ('gpa_med_threshold', 2.5, 'GPA below this is considered Medium Risk'),
            ('max_core_fails', 1.0, 'Maximum allowed core course failures before High Risk')
        ]
        for key, val, desc in default_rules:
            if not RiskRule.query.filter_by(rule_key=key).first():
                db.session.add(RiskRule(rule_key=key, value=val, description=desc))
        
        # Create a default admin if not exists
        if not User.query.filter_by(role='Admin').first():
            admin = User(username='admin', email='admin@nile.edu.ng', role='Admin')
            admin.set_password('admin123')
            db.session.add(admin)
        
        db.session.commit()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
