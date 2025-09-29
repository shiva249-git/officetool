import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

class Config:
    # Get the database URL from environment variable
    database_url = os.environ.get("DATABASE_URL", "sqlite:///office_manager.db")

    # SQLAlchemy requires "postgresql://" instead of "postgres://"
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback_secret")
