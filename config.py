import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    # Get the database URL from environment variable
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///office_manager.db")

    # Replace 'postgres://' with 'postgresql://' for SQLAlchemy compatibility
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key for sessions, forms, etc.
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback_secret")
