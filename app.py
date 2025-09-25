import os
from flask import Flask, redirect, url_for
from config import Config
from extensions import db, login_manager, csrf, migrate
from models import User, Task
from datetime import datetime
from forms.user_forms import LogoutForm
from flask_migrate import upgrade



# Blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.tasks import tasks_bp
from routes.admin import admin_bp

# ------------------ Initialize App ------------------
app = Flask(__name__)
app.config.from_object(Config)

# ------------------ Initialize Extensions ------------------
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
csrf.init_app(app)

with app.app_context():
    try:
        upgrade()  # apply migrations automatically
    except Exception as e:
        print("Migration failed:", e)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL",
    "sqlite:///office_manager.db"  # fallback for local dev
)



# Flask-Login settings
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "warning"

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------ Context Processor ------------------
@app.context_processor
def inject_forms():
    return dict(logout_form=LogoutForm())

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

# ------------------ Routes ------------------
# Redirect root URL to dashboard
@app.route("/")
def index():
    return redirect(url_for("dashboard.home"))

# ------------------ Register Blueprints ------------------
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)  # Already has url_prefix='/dashboard' if defined in blueprint
app.register_blueprint(tasks_bp)
app.register_blueprint(admin_bp)

# ------------------ Run Server ------------------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)



