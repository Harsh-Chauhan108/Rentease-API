
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from dependencies import (
get_current_user,
get_db
)
router = APIRouter(tags=["Properties"])
@router.post("/property")
def add_property(
property: schemas.PropertySchema,
db: Session = Depends(get_db),
current_user = Depends(get_current_user)
):
    if current_user.role != "OWNER":
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
@router.get("/properties")
def get_properties(db: Session = Depends(get_db)):
    properties = db.query(models.Property).all()
    return properties
@router.put("/property/{property_id}")
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
@router.delete("/property/{property_id}")
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