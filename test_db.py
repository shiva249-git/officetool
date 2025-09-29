import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get the database URL
DATABASE_URL = os.environ.get("DATABASE_URL")

# Replace postgres:// with postgresql:// if needed
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

try:
    # Connect to the database
    conn = psycopg2.connect(DATABASE_URL)
    print("✅ Connected successfully!")
    conn.close()
except Exception as e:
    print("❌ Connection failed:")
    print(e)
