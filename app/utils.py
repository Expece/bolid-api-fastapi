from typing import Generator
from app.db.config import Session


def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()