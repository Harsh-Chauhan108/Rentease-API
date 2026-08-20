
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from dependencies import (get_current_user,get_db)
from redis_database import redis_client
import json

router = APIRouter(tags=["Properties"])
@router.post("/property")
async def add_property(
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
    await redis_client.delete("properties")
    return {
    "message": "Property Added"
    }
@router.get("/properties")
async def get_properties(db: Session = Depends(get_db)):
    cached= await redis_client.get("properties")
    if cached:
        return json.loads(cached)
    properties = db.query(models.Property).all()
    result=[]
    for p in properties:
        result.append({
            "id": p.id,
            "title": p.title,
            "city": p.city,
            "rent": p.rent,
            "description": p.description
        })
    await redis_client.set("properties",json.dumps(result),ex=300)
    return result
@router.put("/property/{property_id}")
async def update_property(property_id: int,property: schemas.PropertyUpdate,db: Session = Depends(get_db),current_user = Depends(get_current_user)):

    existing_property = db.query(models.Property).filter(
    models.Property.id == property_id).first()

    if not existing_property:
        raise HTTPException(404, "Property not found")
    if existing_property.owner_id != current_user.id:
        raise HTTPException(403, "Unauthorized")
    updated_data = property.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(existing_property, key, value)
    await redis_client.delete("properties")
    db.commit()
    return {
    "message": "Property Updated"
    }
@router.delete("/property/{property_id}")
async def delete_property(
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
    await redis_client.delete("properties")
    return {
    "message": "Property Deleted"
    }