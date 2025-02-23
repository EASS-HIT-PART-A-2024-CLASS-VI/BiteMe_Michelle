# tests/integration_test.py
import uuid
import pytest
from fastapi.testclient import TestClient

def test_complete_user_flow(test_client):
    """Test complete user registration and order flow"""
    # 1. Register user
    user_data = {
        "email": f"test_{uuid.uuid4().hex[:6]}@example.com",
        "password": "test123",
        "full_name": "Test User",
        "phone_number": "1234567890"
    }
    
    register_response = test_client.post("/users/register", json=user_data)
    assert register_response.status_code == 200
    user_id = register_response.json()["id"]
    
    # 2. Login
    login_response = test_client.post(
        "/users/token",
        data={
            "username": user_data["email"],
            "password": user_data["password"]
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Create restaurant and order
    # First upload a test image file
    import io
    from PIL import Image
    img = Image.new('RGB', (100, 100), color = 'red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    files = {
        'image': ('test.jpg', img_bytes, 'image/jpeg')
    }
    restaurant_data = {
        "name": f"Test Restaurant {uuid.uuid4().hex[:6]}",
        "cuisine_type": "Italian",
        "rating": "4.5",
        "address": "123 Test St",
        "description": "Test Description"
    }
    
    restaurant_response = test_client.post(
        "/restaurants/add",
        data=restaurant_data,
        files=files,
        headers=headers
    )
    assert restaurant_response.status_code == 200
    restaurant = restaurant_response.json()["restaurant"]