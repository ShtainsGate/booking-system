"""Tests for business logic endpoints."""

from fastapi.testclient import TestClient
from app.main import app
from app.schemas.resource import ResourceCreate
from app.schemas.booking import BookingCreate
from datetime import datetime, timedelta
import pytest
from app.database import Base, engine

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """Setup and teardown database for each test."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables after test
    Base.metadata.drop_all(bind=engine)

def get_auth_token():
    """Helper function to get authentication token."""
    user_data = {
        "email": "business@example.com",
        "password": "testpassword123",
        "full_name": "Business User"
    }
    register_response = client.post("/auth/register", json=user_data)
    print(f"Register response: {register_response.status_code}, {register_response.json()}")
    
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    login_response = client.post("/auth/login", data=login_data)
    print(f"Login response: {login_response.status_code}, {login_response.json()}")
    return login_response.json()["access_token"]

def test_create_resource():
    """Test resource creation."""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    resource_data = {
        "name": "Conference Room A",
        "description": "Large conference room with video conferencing",
        "capacity": 20
    }
    
    response = client.post("/resources/", json=resource_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == resource_data["name"]
    assert data["description"] == resource_data["description"]
    assert data["capacity"] == resource_data["capacity"]
    assert data["is_available"] is True
    assert "id" in data

def test_create_booking():
    """Test booking creation."""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # First create a resource
    resource_data = {
        "name": "Meeting Room B",
        "description": "Small meeting room",
        "capacity": 8
    }
    resource_response = client.post("/resources/", json=resource_data, headers=headers)
    resource_id = resource_response.json()["id"]
    
    # Create a booking
    start_time = datetime.now() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)
    
    booking_data = {
        "resource_id": resource_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat()
    }
    
    response = client.post("/bookings/", json=booking_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["resource_id"] == resource_id
    assert data["start_time"] == start_time.isoformat()
    assert data["end_time"] == end_time.isoformat()
    assert "id" in data

def test_booking_conflict():
    """Test booking conflict detection."""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a resource
    resource_data = {
        "name": "Training Room",
        "description": "Training room with projector",
        "capacity": 15
    }
    resource_response = client.post("/resources/", json=resource_data, headers=headers)
    resource_id = resource_response.json()["id"]
    
    # Create first booking
    start_time = datetime.now() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)
    
    booking_data = {
        "resource_id": resource_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat()
    }
    
    # Create first booking
    response = client.post("/bookings/", json=booking_data, headers=headers)
    assert response.status_code == 200
    
    # Try to create overlapping booking
    conflict_booking_data = {
        "resource_id": resource_id,
        "start_time": (start_time + timedelta(minutes=30)).isoformat(),
        "end_time": (end_time + timedelta(minutes=30)).isoformat()
    }
    
    response = client.post("/bookings/", json=conflict_booking_data, headers=headers)
    assert response.status_code == 400
    assert "Time slot already booked" in response.json()["detail"]