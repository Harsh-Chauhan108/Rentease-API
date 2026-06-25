from fastapi import FastAPI
from database import Base, engine
from routers import (
    auth,
    property,
    booking
)
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="RentEase API"
)

app.include_router(auth.router)
app.include_router(property.router)
app.include_router(booking.router)
@app.get("/")
def home():
    return {
    "message": "RentEase API Running"
    }