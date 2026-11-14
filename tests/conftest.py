import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from app.storage import init_db
init_db()
