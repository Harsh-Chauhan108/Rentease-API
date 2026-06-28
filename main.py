from fastapi import FastAPI
from database import Base, engine
from routers import (
    auth,
    property,
    booking
)
from middleware import log_requests
from slowapi.middleware import SlowAPIMiddleware
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="RentEase API"
)

app.add_middleware(SlowAPIMiddleware)
app.middleware("http")(log_requests)
app.include_router(auth.router)
app.include_router(property.router)
app.include_router(booking.router)
@app.get("/")
def home():
    return {
    "message": "RentEase API Running"
    }