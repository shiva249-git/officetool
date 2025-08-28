import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback_secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///office_manager.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
