from app.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
