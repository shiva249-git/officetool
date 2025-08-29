from flask import Flask
from config import Config
from extensions import db, migrate, login_manager, csrf  # import extensions

# Initialize app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
csrf.init_app(app)

# Flask-Login settings
login_manager.login_view = "auth.login"   # redirect unauthorized users to login
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "warning"

# Import models after db is initialized
from models import User, Task

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import and register blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.tasks import tasks_bp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(tasks_bp)

# Run the server
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
