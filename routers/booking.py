

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

@router.put("/booking/{booking_id}/accept")
def accept_booking(booking_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)):

    booking = db.query(models.Booking).filter(
        models.Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(404, "Booking not found")

    property = db.query(models.Property).filter(
        models.Property.id == booking.property_id
    ).first()

    if property.owner_id != current_user.id:
        raise HTTPException(403, "Unauthorized")

    if booking.status != "pending":
        raise HTTPException(400, "Booking already processed")

    booking.status = "accepted"
    db.commit()

    return {"message": "Booking Accepted"}

@router.put("/booking/{booking_id}/reject")
def reject_booking(booking_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)):

    booking = db.query(models.Booking).filter(
        models.Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(404, "Booking not found")

    property = db.query(models.Property).filter(
        models.Property.id == booking.property_id
    ).first()

    if property.owner_id != current_user.id:
        raise HTTPException(403, "Unauthorized")

    if booking.status != "pending":
        raise HTTPException(400, "Booking already processed")

    booking.status = "rejected"
    db.commit()

    return {"message": "Booking Rejected"}

@router.put("/booking/{booking_id}/cancel")
def cancel_booking(booking_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)):

    booking = db.query(models.Booking).filter(
        models.Booking.id == booking_id
    ).first()

    if not booking:
        raise HTTPException(404, "Booking not found")

    if booking.tenant_id != current_user.id:
        raise HTTPException(403, "Unauthorized")

    if booking.status != "pending":
        raise HTTPException(400,
            "Only pending booking can be cancelled")

    booking.status = "cancelled"
    db.commit()

    return {"message": "Booking Cancelled"}

@router.get("/owner/bookings")
def owner_bookings(db: Session = Depends(get_db),
    current_user = Depends(get_current_user)):

    bookings = (db.query(models.Booking).join(models.Property).filter(
            models.Property.owner_id == current_user.id).all())

    return bookings

@router.get("/property/{property_id}/bookings")
def property_bookings(property_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)):
    
    property = db.query(models.Property).filter(
        models.Property.id == property_id
    ).first()

    if not property:
        raise HTTPException(404, "Property not found")

    if property.owner_id != current_user.id:
        raise HTTPException(403, "Unauthorized")

    bookings = db.query(models.Booking).filter(
        models.Booking.property_id == property_id
    ).all()

    return bookings