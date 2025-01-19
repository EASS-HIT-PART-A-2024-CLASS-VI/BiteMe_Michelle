from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to BiteMe!"}

def test_add_menu_item():
    item = {"name": "Burger", "description": "Delicious beef burger", "price": 10.99, "available": True}
    response = client.post("/menu", json=item)
    assert response.status_code == 200
    assert response.json() == {"message": "Item added successfully"}

def test_get_menu():
    response = client.get("/menu")
    assert response.status_code == 200
    assert len(response.json()) > 0
