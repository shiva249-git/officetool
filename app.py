import os
from flask import Flask, redirect, url_for
from config import Config
from extensions import db, login_manager, csrf, migrate
from models import User, Task
from datetime import datetime
from forms.user_forms import LogoutForm
from flask_migrate import upgrade

# Other blueprints
from routes.dashboard import dashboard_bp
from routes.tasks import tasks_bp
from routes.admin import admin_bp

# ------------------ Initialize App ------------------
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Run migrations automatically
    with app.app_context():
        try:
            upgrade()
        except Exception as e:
            print("Migration failed:", e)

    # Flask-Login settings
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"

    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Context processors
    @app.context_processor
    def inject_forms():
        return dict(logout_form=LogoutForm())

    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow}

    # Routes
    @app.route("/")
    def index():
        return redirect(url_for("dashboard.home"))

    # Import auth blueprint here to avoid circular import
    from routes.auth import auth_bp

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(admin_bp)

    return app

