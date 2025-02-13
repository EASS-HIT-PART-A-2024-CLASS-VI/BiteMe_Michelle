# app/api/orders.py
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime
from bson import ObjectId

from app.models.models import Order, OrderStatus, User
from app.core.security import get_current_user
from app.dbConnection.mongoRepository import get_database

router = APIRouter()
db = get_database()

@router.post("/", response_model=Order)
async def create_order(order: Order, current_user: User = Depends(get_current_user)):
    try:
        # Validate restaurant and menu items exist
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

        # Prepare order for database
        order_dict = order.model_dump()  # Changed from dict() to model_dump()
        order_dict['user_id'] = current_user.id
        order_dict['total_price'] = order.total_price
        order_dict['status'] = OrderStatus.PENDING
        order_dict['created_at'] = datetime.utcnow()
        order_dict['updated_at'] = datetime.utcnow()
        
        # Insert order
        result = db["orders"].insert_one(order_dict)
        order_dict['id'] = str(result.inserted_id)
        
        return order_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Order])
async def get_user_orders(current_user: User = Depends(get_current_user)):
    """
    Retrieve all orders for the current user
    """
    orders = list(db["orders"].find({"user_id": current_user.id}))
    # Convert ObjectId to string
    for order in orders:
        order['id'] = str(order['_id'])
    return orders

@router.get("/{order_id}", response_model=Order)
async def get_order_details(
    order_id: str, 
    current_user: User = Depends(get_current_user)
):
    """
    Get details of a specific order
    """
    try:
        order = db["orders"].find_one({"_id": ObjectId(order_id), "user_id": current_user.id})
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        order['id'] = str(order['_id'])
        return order
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
            {"_id": ObjectId(order_id), "user_id": current_user.id},
            {"$set": {
                "status": status, 
                "updated_at": datetime.utcnow()
            }}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return {"message": "Order status updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))