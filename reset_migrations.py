import os
import shutil
from app import app
from extensions import db

def reset_migrations():
    with app.app_context():
        # Drop alembic_version table if it exists
        try:
            db.session.execute('DROP TABLE IF EXISTS alembic_version')
            db.session.commit()
            print("✅ Dropped alembic_version table")
        except Exception as e:
            print(f"⚠️ Could not drop alembic_version: {e}")

    # Remove migrations/versions directory
    versions_path = os.path.join("migrations", "versions")
    if os.path.exists(versions_path):
        shutil.rmtree(versions_path)
        print("✅ Removed migrations/versions folder")

    # Recreate empty versions folder
    os.makedirs(versions_path, exist_ok=True)

    # Run flask db migrate and upgrade automatically
    os.system("flask db migrate -m 'fresh initial migration'")
    os.system("flask db upgrade")

if __name__ == "__main__":
    reset_migrations()
