from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to BiteMe!"}

def test_get_all_restaurants():
    response = client.get("/restaurants")
    assert response.status_code == 200
    assert "restaurants" in response.json()

def test_get_restaurants_by_city():
    response = client.get("/restaurants/get-by-city?city=Tel%20Aviv")
    assert response.status_code == 200
    assert "restaurants" in response.json()

def test_get_restaurants_by_dish():
    response = client.get("/restaurants/get-by-dish?dish_name=Margherita")
    assert response.status_code == 200
    assert "restaurants" in response.json()

def test_get_restaurant_by_name():
    response = client.get("/restaurants/get-by-name?name=Pizza%20Paradise")
    assert response.status_code == 200
    assert "restaurant" in response.json()
