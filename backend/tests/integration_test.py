# tests/integration_test.py
import pytest
import uuid
from fastapi.testclient import TestClient

# Generate unique email for tests
unique_id = str(uuid.uuid4())[:8]
test_user = {
    "email": f"test_{unique_id}@example.com",
    "password": "test123",
    "full_name": "Test Integration User",
    "phone_number": "1234567890"
}

test_restaurant = {
    "id": f"test_{unique_id}",
    "name": f"Integration Test Restaurant {unique_id}",
    "cuisine_type": "Italian",
    "rating": 4.5,
    "address": "123 Test St, Test City",
    "menu": [
        {
            "name": "Test Pizza",
            "description": "A test pizza",
            "price": 45.0,
            "category": "Italian",
            "spiciness_level": 1,
            "is_vegetarian": True,
            "available": True
        }
    ]
}

@pytest.fixture(autouse=True)
def cleanup(test_db):
    # Run the test
    yield
    # Cleanup after test
    test_db["users"].delete_many({"email": test_user["email"]})
    test_db["restaurants"].delete_many({"name": test_restaurant["name"]})
    test_db["orders"].delete_many({"user_id": {"$regex": "test"}})

def test_complete_user_flow(test_client):
    """Test complete user registration and authentication flow"""
    # 1. Register user
    register_response = test_client.post("/users/register", json=test_user)
    assert register_response.status_code == 200
    assert register_response.json()["email"] == test_user["email"]

    # 2. Login
    login_response = test_client.post(
        "/users/token",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

def test_complete_restaurant_flow(test_client):
    """Test complete restaurant creation and management flow"""
    # Create restaurant
    create_response = test_client.post("/restaurants/", json=test_restaurant)
    assert create_response.status_code == 200

    # Get the created restaurant's ID
    restaurant_id = create_response.json()["id"]

    # Get restaurant details
    get_response = test_client.get(f"/restaurants/?cuisine=Italian")
    assert get_response.status_code == 200
    assert len(get_response.json()) > 0

def test_complete_order_flow(test_client):
    """Test complete order creation and management flow"""
    # 1. Register and login
    register_response = test_client.post("/users/register", json=test_user)
    user_id = register_response.json()["id"]

    login_response = test_client.post(
        "/users/token",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    token = login_response.json()["access_token"]

    # 2. Create restaurant
    restaurant = test_client.post("/restaurants/", json=test_restaurant).json()

    # 3. Create order
    order_data = {
        "restaurant_id": restaurant["id"],
        "user_id": user_id,  # Use the actual user ID
        "items": [
            {
                "menu_item_id": "1",
                "restaurant_id": restaurant["id"],
                "name": "Test Pizza",
                "quantity": 2,
                "price": 45.0
            }
        ],
        "total_price": 90.0
    }

    headers = {"Authorization": f"Bearer {token}"}
    order_response = test_client.post("/orders/", json=order_data, headers=headers)
    assert order_response.status_code == 200
    assert "id" in order_response.json()