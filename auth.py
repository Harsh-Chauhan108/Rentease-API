
from database import SessionLocal
from fastapi import Depends, HTTPException, status,FastAPI
from hashing import verify_password, hash_password

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()