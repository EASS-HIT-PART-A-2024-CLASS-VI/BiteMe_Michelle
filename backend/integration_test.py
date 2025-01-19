import httpx

def test_integration():
    base_url = "http://127.0.0.1:8000"

    # Test root endpoint
    response = httpx.get(base_url)
    assert response.status_code == 200

    # Test adding a menu item
    item = {"name": "Pizza", "description": "Cheese pizza", "price": 12.99, "available": True}
    response = httpx.post(f"{base_url}/menu", json=item)
    assert response.status_code == 200

    # Test retrieving the menu
    response = httpx.get(f"{base_url}/menu")
    assert response.status_code == 200
    assert len(response.json()) > 0
