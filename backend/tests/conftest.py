import sys
import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
import uuid
from datetime import datetime

# Add the app directory to Python path
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

try:
    from app.main import app
    from app.dbConnection.mongoRepository import get_database
except ImportError as e:
    print(f"Import Error: {e}")
    print(f"Current sys.path: {sys.path}")
    raise

# Basic fixtures
@pytest.fixture(scope="session")
def test_app():
    """Return the FastAPI app instance"""
    return app

@pytest.fixture(scope="session")
def test_client():
    """Return a TestClient instance"""
    return TestClient(app)

@pytest.fixture(scope="session")
def test_db():
    """Return the test database instance"""
    db = get_database()
    app.state.db = db
    return db

# Test data fixtures
@pytest.fixture
def test_user():
    """Create test user data"""
    unique_id = str(uuid.uuid4())[:8]
    return {
        "email": f"test_{unique_id}@example.com",
        "password": "test123",
        "full_name": "Test User",
        "phone_number": "1234567890"
    }

@pytest.fixture
def test_admin():
    """Create test admin data"""
    return {
        "email": "admin@biteme.com",
        "password": "admin123",
        "full_name": "Admin User",
        "phone_number": "9999999999",
        "is_admin": True
    }

@pytest.fixture
def test_restaurant():
    """Create test restaurant data"""
    unique_id = str(uuid.uuid4())[:8]
    return {
        "id": f"test_{unique_id}",
        "name": f"Test Restaurant {unique_id}",
        "cuisine_type": "Italian",
        "rating": 4.5,
        "address": "123 Test St",
        "description": "Test restaurant description",
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

@pytest.fixture
def test_menu_item():
    """Create test menu item data"""
    return {
        "name": "Test Pizza",
        "description": "A test pizza",
        "price": 45.0,
        "category": "Italian",
        "spiciness_level": 1,
        "is_vegetarian": True,
        "available": True
    }

@pytest.fixture
def test_order():
    """Create test order data"""
    unique_id = str(uuid.uuid4())[:8]
    return {
        "id": f"order_{unique_id}",
        "restaurant_id": f"rest_{unique_id}",
        "items": [
            {
                "menu_item_id": "1",
                "restaurant_id": f"rest_{unique_id}",
                "name": "Test Pizza",
                "quantity": 2,
                "price": 45.0
            }
        ],
        "total_price": 90.0,
        "status": "PENDING"
    }

# Authentication fixtures
@pytest.fixture
def auth_headers(test_client, test_user):
    """Create authentication headers for regular user"""
    # Register user first
    test_client.post("/users/register", json=test_user)
    
    # Get token
    response = test_client.post(
        "/users/token",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_headers(test_client, test_admin):
    """Create authentication headers for admin user"""
    # Register admin first
    test_client.post("/users/register", json=test_admin)
    
    # Get token
    response = test_client.post(
        "/users/token",
        data={
            "username": test_admin["email"],
            "password": test_admin["password"]
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def authenticated_client(test_client, auth_headers):
    """Create an authenticated test client"""
    test_client.headers.update(auth_headers)
    return test_client

@pytest.fixture
def admin_client(test_client, admin_headers):
    """Create an admin authenticated test client"""
    test_client.headers.update(admin_headers)
    return test_client

# Database cleanup
@pytest.fixture(autouse=True)
def cleanup(test_db):
    """Cleanup test data after each test"""
    yield
    # Clean up collections after test
    test_db["users"].delete_many({"email": {"$regex": "test"}})
    test_db["restaurants"].delete_many({"name": {"$regex": "Test Restaurant"}})
    test_db["orders"].delete_many({"id": {"$regex": "order_"}})