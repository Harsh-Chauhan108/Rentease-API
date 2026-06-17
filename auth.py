
from database import SessionLocal,Base,engine
from fastapi import Depends, HTTPException, status,FastAPI
from hashing import verify_password, hash_password
import schemas,models
from sqlalchemy.orm import Session

app=FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register")

def register(user: schemas.RegisterSchema ,
             db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        return {'msg':'User already exists'}
    hashed_password =hash_password(user.password)
    new_user = models.User(name=user.name,email=user.email,password=hashed_password,role=user.role)
    db.add(new_user)
    db.commit()
    return {'msg':'User registered successfully'}
