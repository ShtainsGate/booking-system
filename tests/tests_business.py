"""Tests for business logic endpoints."""

from fastapi.testclient import TestClient
from app.main import app
from app.schemas.resource import ResourceCreate
from app.schemas.booking import BookingCreate
from datetime import datetime, timedelta

client = TestClient(app)

def get_auth_token():
    """Helper function to get authentication token."""
    user_data = {
        "email": "business@example.com",
        "password": "testpassword123",
        "full_name": "Business Test User"
    }
    client.post("/auth/register", json=user_data)
    
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    response = client.post("/auth/login", data=login_data)
    return response.json()["access_token"]

def test_create_resource():
    """Test creating a new resource."""
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
    assert "id" in data

def test_create_booking():
    """Test creating a new booking."""
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
        "end_time": end_time.isoformat(),
        "title": "Team Meeting",
        "description": "Weekly team sync"
    }
    
    response = client.post("/bookings/", json=booking_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["resource_id"] == resource_id
    assert data["title"] == booking_data["title"]
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
        "end_time": end_time.isoformat(),
        "title": "First Meeting",
        "description": "First meeting description"
    }
    client.post("/bookings/", json=booking_data, headers=headers)
    
    # Try to create overlapping booking
    conflict_booking_data = {
        "resource_id": resource_id,
        "start_time": (start_time + timedelta(minutes=30)).isoformat(),
        "end_time": (end_time + timedelta(minutes=30)).isoformat(),
        "title": "Second Meeting",
        "description": "Second meeting description"
    }
    
    response = client.post("/bookings/", json=conflict_booking_data, headers=headers)
    assert response.status_code == 400
    assert "conflict" in response.json()["detail"].lower()

def test_update_booking():
    """Test updating a booking."""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a resource
    resource_data = {
        "name": "Workshop Room",
        "description": "Workshop room with whiteboards",
        "capacity": 12
    }
    resource_response = client.post("/resources/", json=resource_data, headers=headers)
    resource_id = resource_response.json()["id"]
    
    # Create a booking
    start_time = datetime.now() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)
    
    booking_data = {
        "resource_id": resource_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "title": "Initial Title",
        "description": "Initial description"
    }
    booking_response = client.post("/bookings/", json=booking_data, headers=headers)
    booking_id = booking_response.json()["id"]
    
    # Update the booking
    update_data = {
        "title": "Updated Title",
        "description": "Updated description"
    }
    
    response = client.put(f"/bookings/{booking_id}", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"] 