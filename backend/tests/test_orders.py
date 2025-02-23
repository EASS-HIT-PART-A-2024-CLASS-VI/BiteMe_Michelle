# tests/test_orders.py
import uuid
import pytest
from fastapi.testclient import TestClient
import io
from PIL import Image

def test_create_order(test_client, auth_headers):
    """Test creating a new order"""
    # First create a restaurant
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
        headers=auth_headers
    )
    assert restaurant_response.status_code == 200
    restaurant = restaurant_response.json()["restaurant"]
    
    # Add menu item
    menu_item = {
        "name": "Test Pizza",
        "description": "A test pizza",
        "price": "45.0",
        "category": "Italian",
        "spiciness_level": "1",
        "is_vegetarian": "true",
        "available": "true"
    }
    
    menu_response = test_client.post(
        f"/restaurants/{restaurant['id']}/add-item",
        data=menu_item,
        headers=auth_headers
    )
    assert menu_response.status_code == 200
    menu_item_id = menu_response.json()["menu_item"]["id"]
    
    # Create order
    order_data = {
        "restaurant_id": restaurant["id"],
        "items": [
            {
                "menu_item_id": menu_item_id,
                "restaurant_id": restaurant["id"],
                "name": menu_item["name"],
                "quantity": 2,
                "price": float(menu_item["price"])
            }
        ],
        "total_price": float(menu_item["price"]) * 2
    }
    
    response = test_client.post(
        "/orders/",
        json=order_data,
        headers=auth_headers
    )
    assert response.status_code == 200

def test_get_user_orders(test_client, auth_headers):
    """Test retrieving user's orders"""
    response = test_client.get("/orders/", headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)