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
def admin_headers(test_client, test_db, test_admin):
    """Create authentication headers for admin user"""
    # Check if user already exists, if so, try to get token directly
    existing_user = test_db["users"].find_one({"email": test_admin["email"]})

    if existing_user:
        # If user exists, attempt to get token
        login_response = test_client.post(
            "/users/token",
            data={
                "username": test_admin["email"],
                "password": test_admin["password"]
            }
        )
    else:
        # Register user first
        register_response = test_client.post("/users/register", json={
            "email": test_admin["email"],
            "password": test_admin["password"],
            "full_name": test_admin["full_name"],
            "phone_number": test_admin["phone_number"]
        })

        # Verify registration was successful
        assert register_response.status_code == 200, f"Registration failed: {register_response.text}"

        # Attempt to login
        login_response = test_client.post(
            "/users/token",
            data={
                "username": test_admin["email"],
                "password": test_admin["password"]
            }
        )

    # Verify login was successful
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"

    # Manually update user to admin in the database
    update_result = test_db["users"].update_one(
        {"email": test_admin["email"]},
        {"$set": {"is_admin": True}}
    )

    # Verify the update was successful
    assert update_result.modified_count >= 0, "Failed to set admin status"

    # Get token from login response
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# Keep the test_admin fixture as is
@pytest.fixture
def test_admin():
    """Create test admin data"""
    return {
        "email": "admin@biteme.com",
        "password": "admin",
        "full_name": "Admin User",
        "phone_number": "9999999999"
    }
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