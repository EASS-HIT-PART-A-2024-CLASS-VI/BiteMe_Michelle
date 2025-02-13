# tests/unit_test.py
import pytest
from fastapi.testclient import TestClient
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.models import Restaurant, MenuItem, Order, User
from app.main import app

client = TestClient(app)

def test_password_hashing():
    """Test password hashing functionality"""
    password = "testpassword123"
    hashed = get_password_hash(password)
    
    assert hashed != password
    assert verify_password(password, hashed) == True
    assert verify_password("wrongpassword", hashed) == False

def test_token_creation():
    """Test access token creation"""
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    
    assert isinstance(token, str)
    assert len(token) > 0

def test_order_validation():
    """Test Order model validation"""
    valid_order = {
        "id": "1",
        "user_id": "user_1",
        "restaurant_id": "rest_1",  # Added missing restaurant_id
        "items": [
            {
                "menu_item_id": "1",
                "restaurant_id": "rest_1",
                "name": "Test Item",
                "quantity": 2,
                "price": 10.0
            }
        ],
        "total_price": 20.0,
        "status": "PENDING"
    }
    order = Order(**valid_order)
    assert order.total_price == 20.0
    
    # Test invalid order (negative price)
    invalid_order = valid_order.copy()
    invalid_order["total_price"] = -10.0
    with pytest.raises(ValueError):
        Order(**invalid_order)
        
    # Test invalid quantity
    invalid_order = valid_order.copy()
    invalid_order["items"][0]["quantity"] = 0
    with pytest.raises(ValueError):
        Order(**invalid_order)
        
    # Test missing required field
    invalid_order = valid_order.copy()
    del invalid_order["restaurant_id"]
    with pytest.raises(ValueError):
        Order(**invalid_order)

def test_restaurant_model_validation():
    """Test Restaurant model validation"""
    valid_restaurant = {
        "id": "1",
        "name": "Test Restaurant",
        "cuisine_type": "Italian",
        "rating": 4.5,
        "address": "Test Address",
        "menu": [
            {
                "name": "Test Item",
                "description": "Test Description",
                "price": 10.0,
                "category": "Italian",
                "is_vegetarian": True,
                "available": True
            }
        ]
    }
    restaurant = Restaurant(**valid_restaurant)
    assert restaurant.name == "Test Restaurant"
    assert len(restaurant.menu) == 1

def test_menu_item_validation():
    """Test MenuItem model validation"""
    valid_item = {
        "name": "Test Item",
        "description": "Test Description",
        "price": 10.0,
        "category": "Italian",
        "spiciness_level": 3,
        "is_vegetarian": True,
        "available": True
    }
    menu_item = MenuItem(**valid_item)
    assert menu_item.price == 10.0

def test_root_endpoint(test_client):
    """Test root endpoint"""
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to BiteMe!"}

def test_health_check(test_client):
    """Test health check endpoint"""
    response = test_client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()

def test_db_connection(test_client, test_db):
    """Test database connection"""
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"