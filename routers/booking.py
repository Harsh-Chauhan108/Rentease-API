

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from dependencies import (
get_current_user,
get_db
)
router = APIRouter(tags=["Bookings"])
@router.post("/booking")

def create_booking(
booking: schemas.BookingSchema,
db: Session = Depends(get_db),
current_user = Depends(get_current_user)
):
    if current_user.role != "TENANT":
        raise HTTPException(
        403,
        "Only tenants can book properties"
        )
    property = db.query(models.Property).filter(
    models.Property.id == booking.property_id
    ).first()
    if not property:
        raise HTTPException(404, "Property not found")
    new_booking = models.Booking(
    tenant_id=current_user.id,
    property_id=booking.property_id
    )
    db.add(new_booking)
    db.commit()
    return {
    "message": "Booking Request Sent"
    }
@router.get("/my-bookings")
def my_bookings(
db: Session = Depends(get_db),
current_user = Depends(get_current_user)
):
    bookings = db.query(models.Booking).filter(
    models.Booking.tenant_id == current_user.id
    ).all()
    return bookings