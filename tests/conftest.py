import os
import pytest

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from app.db import Base, engine
from app.storage import init_db
init_db()

@pytest.fixture(autouse=True)
def clean_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
