# tests/test_users.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

def test_user_registration(test_client):
    """Test user registration"""
    user_data = {
        "email": f"test_{uuid.uuid4().hex[:6]}@example.com",
        "password": "test123",
        "full_name": "Test User",
        "phone_number": "1234567890"
    }
    
    response = test_client.post("/users/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == user_data["email"]
    assert "id" in response.json()

def test_user_login(test_client, test_user):
    """Test user login"""
    # First register the user
    test_client.post("/users/register", json=test_user)
    
    # Try logging in
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    
    response = test_client.post("/users/token", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_user_profile(test_client, auth_headers):
    """Test getting user profile"""
    response = test_client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    assert "email" in response.json()

def test_update_user_profile(test_client, auth_headers):
    """Test updating user profile"""
    update_data = {
        "full_name": "Updated Name",
        "phone_number": "9876543210"
    }
    
    response = test_client.put("/users/me", 
                             json=update_data,
                             headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["full_name"] == update_data["full_name"]