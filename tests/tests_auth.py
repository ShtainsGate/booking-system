"""Tests for authentication endpoints."""

from fastapi.testclient import TestClient
from app.main import app
from app.schemas.user import UserCreate
from app.crud.user import get_user_by_email
from app.database import get_db
from sqlalchemy.orm import Session

client = TestClient(app)

def test_register_user():
    """Test user registration endpoint."""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data

def test_register_duplicate_email():
    """Test registration with duplicate email."""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    # First registration
    client.post("/auth/register", json=user_data)
    # Second registration with same email
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400

def test_login_user():
    """Test user login endpoint."""
    # First register a user
    user_data = {
        "email": "login@example.com",
        "password": "testpassword123",
        "full_name": "Login User"
    }
    client.post("/auth/register", json=user_data)
    
    # Then try to login
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password():
    """Test login with wrong password."""
    user_data = {
        "email": "wrongpass@example.com",
        "password": "testpassword123",
        "full_name": "Wrong Pass User"
    }
    client.post("/auth/register", json=user_data)
    
    login_data = {
        "username": user_data["email"],
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 401

def test_protected_endpoint():
    """Test access to protected endpoint."""
    # Register and login
    user_data = {
        "email": "protected@example.com",
        "password": "testpassword123",
        "full_name": "Protected User"
    }
    client.post("/auth/register", json=user_data)
    
    login_data = {
        "username": user_data["email"],
        "password": user_data["password"]
    }
    login_response = client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]
    
    # Try to access protected endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/resources/", headers=headers)
    assert response.status_code == 200