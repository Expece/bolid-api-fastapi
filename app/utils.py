from app.db.config import Session


def get_db():
    """Connect to database and return session"""
    try:
        db = Session()
        yield db
    finally:
        db.close()