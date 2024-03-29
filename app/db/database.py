from app.db.loader import load_db
from app.schemas.database import Database

db = load_db()


def get_db() -> Database:
    return db
