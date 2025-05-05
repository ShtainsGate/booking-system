"""Main application module for the Booking System.

This module initializes the FastAPI application and sets up all necessary routers
for handling authentication, resources, and bookings.
"""

from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth_router, resources_router, bookings_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "persistAuthorization": True  # Сохраняет токен после перезагрузки
    }
)

app.include_router(auth_router)
app.include_router(resources_router)
app.include_router(bookings_router)

@app.get("/")
def read_root():
    """Root endpoint that returns a welcome message.
    
    Returns:
        dict: A welcome message for the Booking System.
    """
    return {"message": "Welcome to the Booking System!"}