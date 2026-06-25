
from database import SessionLocal,Base,engine
from fastapi import Depends, HTTPException, status
from hashing import verify_password, hash_password
import schemas,models
from sqlalchemy.orm import Session
from fastapi.requests import Request
from fastapi import APIRouter
from tokens import (
    create_access_token,
    create_refresh_token,
    SECRET_KEY,
    ALGORITHM
)
from jose import jwt

router = APIRouter(tags=["Authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")

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


from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    if not existing_user:
        raise HTTPException(404, "User Not Found")

    if not verify_password(
        form_data.password,
        existing_user.password
    ):
        raise HTTPException(401, "Wrong Password")

    access_token = create_access_token({
        "id": existing_user.id
    })

    refresh_token = create_refresh_token({
        "id": existing_user.id
    })

    existing_user.refresh_token = refresh_token
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
@router.post("/refresh")
def refresh_token(
refresh_token: str,
db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
        refresh_token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
        )
        user_id = payload.get("id")
    except:
        raise HTTPException(
        401,
        "Invalid Refresh Token"
        )
    user = db.query(models.User).filter(
    models.User.id == user_id
    ).first()
    if not user:
        raise HTTPException(404, "User not found")
    if user.refresh_token != refresh_token:
        raise HTTPException(
        401,
        "Token mismatch"
        )
    new_access_token = create_access_token({
    "id": user.id
    })
    return {
    "access_token": new_access_token
    }

@router.post("/logout")
def logout(
refresh_token: str,
db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
    models.User.refresh_token == refresh_token
    ).first()
    if not user:
        raise HTTPException(404, "User not found")
    user.refresh_token = None
    db.commit()
    return {
    "message": "Logged out successfully"
    }

from dependencies import (
    get_current_user,
    get_db
)



