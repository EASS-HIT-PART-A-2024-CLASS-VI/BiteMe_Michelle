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

def test_get_restaurants_by_city():
    base_url = "http://127.0.0.1:8000"
    response = httpx.get(f"{base_url}/restaurants/get-by-city?city=Tel%20Aviv")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_place_order():
    base_url = "http://127.0.0.1:8000"
    order_payload = {"restaurant_id": 1, "dish_name": "Margherita", "quantity": 2, "customer_name": "John Doe"}
    response = httpx.post(f"{base_url}/submit/place-order", json=order_payload)
    assert response.status_code == 200
    assert "message" in response.json()
