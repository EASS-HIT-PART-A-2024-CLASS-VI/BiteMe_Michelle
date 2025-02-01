import pytest
from fastapi.testclient import TestClient
from app.main import app

# Initialize the TestClient
client = TestClient(app)

def test_root_endpoint():
    """
    Test the root endpoint of the API.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to BiteMe!"}

def test_fetch_all_restaurants():
    """
    Test fetching all restaurants from the database.
    """
    response = client.get("/restaurants")
    assert response.status_code == 200
    assert "restaurants" in response.json()
    assert len(response.json()["restaurants"]) > 0  # Ensure restaurants are returned

def test_fetch_restaurants_by_city():
    """
    Test fetching restaurants filtered by city.
    """
    response = client.get("/restaurants/get-by-city?city=Tel%20Aviv")
    assert response.status_code == 200
    assert "restaurants" in response.json()
    assert len(response.json()["restaurants"]) > 0  # Ensure results exist

def test_fetch_restaurants_by_dish():
    """
    Test fetching restaurants that serve a specific dish.
    """
    response = client.get("/restaurants/get-by-dish?dish_name=Margherita")
    assert response.status_code == 200
    assert "restaurants" in response.json()
    assert len(response.json()["restaurants"]) > 0  # Ensure results exist

def test_fetch_restaurant_by_name():
    """
    Test fetching a restaurant by its name.
    """
    response = client.get("/restaurants/get-by-name?name=Pizza%20Paradise")
    assert response.status_code == 200
    assert "restaurant" in response.json()
    assert response.json()["restaurant"]["name"] == "Pizza Paradise"
