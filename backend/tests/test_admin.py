# tests/test_admin.py
import uuid
import pytest
from fastapi.testclient import TestClient
import io
from PIL import Image

def test_admin_create_restaurant(test_client, admin_headers):
    """Test admin creating a restaurant"""
    # Create test image
    img = Image.new('RGB', (100, 100), color = 'red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)

    files = {
        'image': ('test.jpg', img_bytes, 'image/jpeg')
    }
    test_data = {
        "name": f"Test Restaurant {uuid.uuid4().hex[:6]}",
        "cuisine_type": "Italian",
        "rating": "4.5",
        "address": "123 Test St",
        "description": "Test Description"
    }

    # Verify admin headers are set correctly
    assert "Authorization" in admin_headers, "Authorization headers not set"

    response = test_client.post(
        "/restaurants/add",
        data=test_data,
        files=files,
        headers=admin_headers
    )

    # Add detailed error logging
    if response.status_code != 200:
        print("Restaurant Creation Failed")
        print("Response Status:", response.status_code)
        print("Response Headers:", response.headers)
        print("Response Content:", response.text)

    assert response.status_code == 200, "Failed to create restaurant"
    assert "restaurant" in response.json()
    assert response.json()["restaurant"]["name"] == test_data["name"]

def test_admin_update_restaurant(test_client, admin_headers):
    """Test admin updating a restaurant"""
    # First create a restaurant with image
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
        "description": "Original Description"
    }

    create_response = test_client.post(
        "/restaurants/add",
        data=restaurant_data,
        files=files,
        headers=admin_headers
    )

    # Verify restaurant creation
    assert create_response.status_code == 200, "Failed to create restaurant for update test"
    restaurant_id = create_response.json()["restaurant"]["id"]

    # Update the restaurant
    update_data = {
        "name": restaurant_data["name"],
        "cuisine_type": "French",
        "rating": "4.8",
        "address": "456 New St",
        "description": "Updated Description"
    }

    response = test_client.put(
        f"/restaurants/{restaurant_id}",
        data=update_data,
        headers=admin_headers
    )

    # Add detailed error logging
    if response.status_code != 200:
        print("Restaurant Update Failed")
        print("Response Status:", response.status_code)
        print("Response Headers:", response.headers)
        print("Response Content:", response.text)

    assert response.status_code == 200, "Failed to update restaurant"
    assert response.json()["cuisine_type"] == "French"
    assert response.json()["rating"] == 4.8

def test_admin_add_menu_item(test_client, admin_headers):
    """Test adding a menu item to a restaurant"""
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
        headers=admin_headers
    )
    assert restaurant_response.status_code == 200, "Failed to create restaurant for menu item test"
    restaurant_id = restaurant_response.json()["restaurant"]["id"]

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

    response = test_client.post(
        f"/restaurants/{restaurant_id}/add-item",
        data=menu_item,
        headers=admin_headers
    )

    # Add detailed error logging
    if response.status_code != 200:
        print("Add Menu Item Failed")
        print("Response Status:", response.status_code)
        print("Response Headers:", response.headers)
        print("Response Content:", response.text)

    assert response.status_code == 200, "Failed to add menu item"
    assert response.json()["menu_item"]["name"] == "Test Pizza"
    assert response.json()["menu_item"]["price"] == 45.0

def test_admin_delete_menu_item(test_client, admin_headers):
    """Test deleting a menu item from a restaurant"""
    # First create a restaurant with a menu item
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
        headers=admin_headers
    )
    restaurant_id = restaurant_response.json()["restaurant"]["id"]

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
        f"/restaurants/{restaurant_id}/add-item",
        data=menu_item,
        headers=admin_headers
    )
    menu_item_name = menu_response.json()["menu_item"]["name"]

    # Delete menu item using name instead of ID
    response = test_client.delete(
        f"/restaurants/{restaurant_id}/menu/{menu_item_name}",
        headers=admin_headers
    )

    # Add detailed error logging
    if response.status_code != 200:
        print("Delete Menu Item Failed")
        print("Response Status:", response.status_code)
        print("Response Headers:", response.headers)
        print("Response Content:", response.text)

    assert response.status_code == 200, "Failed to delete menu item"
    assert "successfully" in response.json()["message"].lower()

def test_admin_delete_restaurant(test_client, admin_headers):
    """Test deleting a restaurant"""
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

    create_response = test_client.post(
        "/restaurants/add",
        data=restaurant_data,
        files=files,
        headers=admin_headers
    )
    restaurant_id = create_response.json()["restaurant"]["id"]

    # Delete the restaurant
    response = test_client.delete(
        f"/restaurants/{restaurant_id}",
        headers=admin_headers
    )

    # Add detailed error logging
    if response.status_code != 200:
        print("Delete Restaurant Failed")
        print("Response Status:", response.status_code)
        print("Response Headers:", response.headers)
        print("Response Content:", response.text)

    assert response.status_code == 200, "Failed to delete restaurant"
    assert "successfully" in response.json()["message"].lower()