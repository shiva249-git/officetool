from app import app, db
from models import User  # Make sure your User model is correctly imported
from werkzeug.security import generate_password_hash

# Admin credentials
admin_email = "shivathota01@gmail.com"
admin_username = "admin"
admin_password = "shiva123"

with app.app_context():
    # Drop all tables
    print("Dropping all tables...")
    db.drop_all()

    # Create all tables
    print("Creating tables...")
    db.create_all()

    # Create admin user
    print("Creating admin user...")
    admin_user = User(
        username=admin_username,
        email=admin_email,
        password_hash=generate_password_hash(admin_password),
        is_admin=True
    )

    db.session.add(admin_user)
    db.session.commit()
    print("Admin user created successfully!")
