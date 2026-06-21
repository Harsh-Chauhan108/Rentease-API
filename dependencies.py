from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal
from auth import SECRET_KEY, ALGORITHM
import models
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(401, "Invalid Token")
    except JWTError:
        raise HTTPException(401, "Invalid Token")
    user = db.query(models.User).filter(
        models.User.id == user_id
    ).first()
    if not user:
        raise HTTPException(404, "User not found")
    return user