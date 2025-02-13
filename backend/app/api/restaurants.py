# app/api/restaurants.py
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.models.models import Restaurant, MenuItem, FoodCategory
from app.dbConnection.mongoRepository import get_database
from bson import ObjectId
import uuid

router = APIRouter()
db = get_database()

@router.post("/", response_model=Restaurant)
async def create_restaurant(restaurant: Restaurant):
    try:
        existing = db["restaurants"].find_one({"name": restaurant.name})
        if existing:
            raise HTTPException(status_code=400, detail="Restaurant already exists")
        
        restaurant_id = str(uuid.uuid4())
        restaurant_dict = restaurant.model_dump()  # Changed from dict() to model_dump()
        restaurant_dict["id"] = restaurant_id
        
        result = db["restaurants"].insert_one(restaurant_dict)
        
        return restaurant_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{restaurant_id}", response_model=Restaurant)
async def update_restaurant_details(restaurant_id: str, restaurant: Restaurant):
    try:
        result = db["restaurants"].update_one(
            {"id": restaurant_id},
            {"$set": restaurant.model_dump(exclude={"id"})}  # Changed from dict() to model_dump()
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        
        updated_restaurant = db["restaurants"].find_one({"id": restaurant_id})
        return updated_restaurant
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{restaurant_id}")
async def delete_restaurant(restaurant_id: str):
    try:
        result = db["restaurants"].delete_one({"id": restaurant_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        
        return {"message": "Restaurant deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Restaurant])
async def get_restaurants(
    cuisine: Optional[FoodCategory] = None,
    min_rating: Optional[float] = None
):
    try:
        query = {}
        if cuisine:
            query["cuisine_type"] = cuisine
        if min_rating:
            query["rating"] = {"$gte": min_rating}
        
        restaurants = list(db["restaurants"].find(query))
        return restaurants
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{restaurant_name}/menu", response_model=Restaurant)
async def add_menu_item(restaurant_name: str, menu_item: MenuItem):
    try:
        result = db["restaurants"].update_one(
            {"name": restaurant_name},
            {"$push": {"menu": menu_item.model_dump()}}  # Changed from dict() to model_dump()
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        
        updated_restaurant = db["restaurants"].find_one({"name": restaurant_name})
        return updated_restaurant
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{restaurant_name}/menu/{menu_item_name}", response_model=Restaurant)
async def update_menu_item(
    restaurant_name: str, 
    menu_item_name: str, 
    updated_item: MenuItem
):
    try:
        result = db["restaurants"].update_one(
            {
                "name": restaurant_name, 
                "menu.name": menu_item_name
            },
            {"$set": {"menu.$": updated_item.model_dump()}}  # Changed from dict() to model_dump()
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Restaurant or menu item not found")
        
        updated_restaurant = db["restaurants"].find_one({"name": restaurant_name})
        return updated_restaurant
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{restaurant_name}/menu/{menu_item_name}")
async def delete_menu_item(restaurant_name: str, menu_item_name: str):
    try:
        result = db["restaurants"].update_one(
            {"name": restaurant_name},
            {"$pull": {"menu": {"name": menu_item_name}}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Restaurant or menu item not found")
            
        return {"message": f"Menu item '{menu_item_name}' deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))