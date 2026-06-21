
from database import SessionLocal,Base,engine
from fastapi import Depends, HTTPException, status,FastAPI
from hashing import verify_password, hash_password
import schemas,models
from sqlalchemy.orm import Session
from tokens import create_access_token,create_refresh_token
from fastapi.requests import Request

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

@app.post("/login")
def login(
    request: Request,
    user: schemas.LoginSchema,
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(
    models.User.email == user.email
    ).first()
    if not existing_user:
        return {'msg': "User Not Found"}
    if not verify_password(
    user.password,
    existing_user.password
    ):
        return {'msg': "Wrong Password"}
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
@app.post("/logout")
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


@app.post("/property")
def add_property(
property: schemas.PropertySchema,
db: Session = Depends(get_db),
current_user = Depends(get_current_user)
):
    if current_user.role != "owner":
        raise HTTPException(403,
          "Only owners can add property"
        )
    new_property = models.Property(
    **property.dict(),
    owner_id=current_user.id
    )
    db.add(new_property)
    db.commit()
    return {
    "message": "Property Added"
    }
@app.get("/properties")
def get_properties(db: Session = Depends(get_db)):
    properties = db.query(models.Property).all()
    return properties
@app.put("/property/{property_id}")
def update_property(
property_id: int,
property: schemas.PropertySchema,
db: Session = Depends(get_db),
current_user = Depends(get_current_user)
):
    existing_property = db.query(models.Property).filter(
    models.Property.id == property_id
    ).first()
    if not existing_property:
        raise HTTPException(404, "Property not found")
    if existing_property.owner_id != current_user.id:
        raise HTTPException(403, "Unauthorized")
    existing_property.title = property.title
    existing_property.city = property.city
    existing_property.rent = property.rent
    existing_property.description = property.description
    db.commit()
    return {
    "message": "Property Updated"
    }
@app.delete("/property/{property_id}")
def delete_property(
property_id: int,
db: Session = Depends(get_db),
current_user = Depends(get_current_user)
):
    property = db.query(models.Property).filter(
    models.Property.id == property_id
    ).first()
    if not property:
        raise HTTPException(404, "Property not found")
    if property.owner_id != current_user.id:
        raise HTTPException(403, "Unauthorized")
    db.delete(property)
    db.commit()
    return {
    "message": "Property Deleted"
    }