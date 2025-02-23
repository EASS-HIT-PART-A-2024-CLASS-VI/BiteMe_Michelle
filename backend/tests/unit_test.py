# tests/unit_test.py
import pytest
from app.core.security import verify_password, get_password_hash
from app.models.models import Order, Restaurant, MenuItem

def test_order_model_validation():
    """Test Order model validation"""
    valid_order = {
        "id": "1",
        "user_id": "user_1",
        "restaurant_id": "rest_1",
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