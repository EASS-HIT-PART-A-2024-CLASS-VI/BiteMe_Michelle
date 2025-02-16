from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
from bson import ObjectId
import uuid

from app.models.models import Order, OrderStatus, User, OrderItem
from app.core.security import get_current_user
from app.dbConnection.mongoRepository import get_database

router = APIRouter()
db = get_database()

@router.post("/", response_model=Order)
async def create_order(order: Order, current_user: User = Depends(get_current_user)):
    try:
        # Validate restaurant and menu items exist
        restaurant_ids = set()
        for item in order.items:
            # Check restaurant exists
            restaurant = db["restaurants"].find_one({"id": item.restaurant_id})
            if not restaurant:
                raise HTTPException(status_code=404,
                                    detail=f"Restaurant {item.restaurant_id} not found")

            # Check menu item exists and price matches
            menu_item = next((m for m in restaurant.get('menu', [])
                              if m.get('name') == item.name), None)
            if not menu_item:
                raise HTTPException(status_code=404,
                                    detail=f"Menu item {item.name} not found in restaurant")

            # Validate menu item price
            if abs(float(menu_item['price']) - item.price) > 0.01:
                raise HTTPException(status_code=400,
                                    detail=f"Price mismatch for {item.name}")

            # Collect unique restaurant IDs
            restaurant_ids.add(item.restaurant_id)

        # Prepare order for database
        order_dict = order.model_dump()

        # Use provided ID or generate a new one
        if not order_dict.get('id'):
            order_dict['id'] = str(uuid.uuid4())

        # Set user ID
        order_dict['user_id'] = current_user.id

        # Set restaurant ID (use first restaurant if multiple)
        if not order_dict.get('restaurant_id') and restaurant_ids:
            order_dict['restaurant_id'] = list(restaurant_ids)[0]

        # Ensure status and timestamps
        order_dict['status'] = OrderStatus.PENDING
        order_dict['created_at'] = datetime.utcnow()
        order_dict['updated_at'] = datetime.utcnow()

        # Insert order
        result = db["orders"].insert_one(order_dict)

        return order_dict
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Order])
async def get_user_orders(current_user: User = Depends(get_current_user)):
    """
    Retrieve all orders for the current user
    """
    try:
        # Find orders for the current user
        orders = list(db["orders"].find({"user_id": current_user.id}))

        # Convert database representation to Order model
        processed_orders = []
        for order in orders:
            # Ensure 'id' is a string
            order['id'] = str(order.get('id') or order.get('_id'))
            processed_orders.append(order)

        # Sort orders by creation date, most recent first
        processed_orders.sort(key=lambda x: x.get('created_at', datetime.min), reverse=True)

        return processed_orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {str(e)}")

@router.get("/{order_id}", response_model=Order)
async def get_order_details(
        order_id: str,
        current_user: User = Depends(get_current_user)
):
    """
    Get details of a specific order
    """
    try:
        # Try to find the order by ID
        order = db["orders"].find_one({
            "$or": [
                {"_id": ObjectId(order_id)},
                {"id": order_id}
            ],
            "user_id": current_user.id
        })

        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        # Ensure 'id' is a string
        order['id'] = str(order.get('id') or order.get('_id'))

        return order
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid order ID")

@router.put("/{order_id}/status")
async def update_order_status(
        order_id: str,
        status: OrderStatus,
        current_user: User = Depends(get_current_user)
):
    """
    Update order status
    """
    try:
        result = db["orders"].update_one(
            {
                "$or": [
                    {"_id": ObjectId(order_id)},
                    {"id": order_id}
                ],
                "user_id": current_user.id
            },
            {"$set": {
                "status": status,
                "updated_at": datetime.utcnow()
            }}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Order not found")

        return {"message": "Order status updated successfully"}
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))