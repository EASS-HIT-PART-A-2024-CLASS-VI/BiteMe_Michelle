from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from app.models.models import Restaurant, MenuItem, FoodCategory, User
from app.dbConnection.mongoRepository import get_database
from app.core.security import get_current_admin
from bson import ObjectId
import uuid
import logging
from urllib.parse import unquote
from fastapi import File, UploadFile, Form
import os
import shutil
from datetime import datetime
import json


router = APIRouter()
db = get_database()

# Configure logging
logging.basicConfig(
    level=logging.ERROR,  # Only log errors and critical messages
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define the correct static folder path
UPLOAD_DIR = "static/restaurant_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class MongoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

def serialize_mongo_doc(doc):
    if doc.get('_id'):
        doc['_id'] = str(doc['_id'])
    return doc


@router.put("/{restaurant_id}")
async def update_restaurant(
        restaurant_id: str,
        name: str = Form(...),
        cuisine_type: str = Form(...),
        rating: float = Form(...),
        address: str = Form(...),
        description: Optional[str] = Form("")
):
    try:
        print(f"Updating restaurant {restaurant_id}")
        print(f"Update data: {name}, {cuisine_type}, {rating}, {address}, {description}")

        # Prepare update data
        update_data = {
            "name": name,
            "cuisine_type": cuisine_type,
            "rating": float(rating),
            "address": address,
            "description": description or "",
            "updated_at": datetime.utcnow()
        }

        # Update restaurant
        result = db["restaurants"].update_one(
            {"id": restaurant_id},
            {"$set": update_data}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        # Get updated restaurant
        updated_restaurant = db["restaurants"].find_one({"id": restaurant_id})
        if not updated_restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        return serialize_mongo_doc(updated_restaurant)

    except Exception as e:
        print(f"Error updating restaurant: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update restaurant: {str(e)}"
        )

@router.delete("/{restaurant_id}")
async def delete_restaurant(
        restaurant_id: str,
        current_admin: User = Depends(get_current_admin)
):
    try:
        logger.info(f"Deleting restaurant: {restaurant_id}")

        # Delete restaurant from database
        result = db["restaurants"].delete_one({"id": restaurant_id})

        logger.info(f"Delete result: {result.deleted_count}")

        if result.deleted_count == 0:
            logger.error(f"Restaurant not found: {restaurant_id}")
            raise HTTPException(status_code=404, detail="Restaurant not found")

        return {"message": "Restaurant deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting restaurant: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting restaurant: {str(e)}")

# In restaurants.py
@router.delete("/{restaurant_id}/menu/{item_name}")
async def delete_menu_item(
        restaurant_id: str,
        item_name: str
):
    try:
        # Decode the item name
        item_name = unquote(item_name)

        print(f"Delete Menu Item Request - Restaurant ID: {restaurant_id}")
        print(f"Delete Menu Item Request - Item Name: {item_name}")

        # Find the restaurant first
        restaurant = db["restaurants"].find_one({"id": restaurant_id})
        if not restaurant:
            print(f"Restaurant not found: {restaurant_id}")
            raise HTTPException(status_code=404, detail=f"Restaurant not found: {restaurant_id}")

        # Remove the menu item
        result = db["restaurants"].update_one(
            {"id": restaurant_id},
            {
                "$pull": {"menu": {"name": item_name}}
            }
        )

        if result.modified_count == 0:
            print(f"Failed to delete menu item: {item_name}")
            raise HTTPException(status_code=404, detail="Failed to delete menu item")

        print(f"Menu item '{item_name}' deleted successfully")
        return {"message": f"Menu item '{item_name}' deleted successfully"}
    except Exception as e:
        print(f"Unexpected error deleting menu item: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_restaurants():
    try:
        restaurants = list(db["restaurants"].find())

        # Convert ObjectId to string
        for restaurant in restaurants:
            restaurant["_id"] = str(restaurant["_id"])

        return restaurants
    except Exception as e:
        logger.error(f"Error in get_restaurants: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Add a new restaurant

@router.post("/add")  # Changed from /restaurants/add since the prefix is already /restaurants
async def add_restaurant(
        name: str = Form(...),
        cuisine_type: str = Form(...),
        rating: float = Form(...),
        address: str = Form(...),
        description: Optional[str] = Form(None),
        image: UploadFile = File(...)
):
    try:
        print(f"Received request to add restaurant: {name}")

        # Generate unique restaurant ID
        restaurant_id = str(uuid.uuid4())

        # Handle image upload
        file_extension = os.path.splitext(image.filename)[1]
        image_filename = f"{restaurant_id}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, image_filename)

        print(f"Saving image to: {file_path}")

        # Save the uploaded image
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # Create restaurant data
        restaurant_data = {
            "id": restaurant_id,
            "name": name,
            "cuisine_type": cuisine_type,
            "rating": float(rating),
            "address": address,
            "description": description or "",
            "menu": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        print(f"Inserting restaurant data: {restaurant_data}")

        # Save the image_url in the database but don't include in response
        db_restaurant_data = {
            **restaurant_data,
            "image_url": f"/static/restaurant_images/{image_filename}"
        }

        # Insert into database
        result = db["restaurants"].insert_one(restaurant_data)

        # Convert ObjectId to string before returning
        restaurant_data['_id'] = str(result.inserted_id)

        return {
            "message": "Restaurant added successfully",
            "restaurant": restaurant_data
        }

    except Exception as e:
        print(f"Error adding restaurant: {str(e)}")
        # If there's an error, clean up any uploaded file
        if 'file_path' in locals():
            try:
                os.remove(file_path)
            except:
                pass
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add restaurant: {str(e)}"
        )
@router.post("/{restaurant_id}/add-item")
async def add_menu_item(
        restaurant_id: str,
        name: str = Form(...),
        description: str = Form(...),
        price: float = Form(...),
        category: str = Form(...),
        spiciness_level: int = Form(1),
        is_vegetarian: bool = Form(False),
        available: bool = Form(True)
):
    try:
        print(f"Adding menu item to restaurant {restaurant_id}")

        # Check if restaurant exists
        restaurant = db["restaurants"].find_one({"id": restaurant_id})
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        # Create menu item
        menu_item = {
            "id": str(uuid.uuid4()),
            "name": name,
            "description": description,
            "price": float(price),
            "category": category,
            "spiciness_level": spiciness_level,
            "is_vegetarian": is_vegetarian,
            "available": available
        }

        # Add menu item to restaurant
        result = db["restaurants"].update_one(
            {"id": restaurant_id},
            {
                "$push": {"menu": menu_item},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="Failed to add menu item")

        print(f"Successfully added menu item: {menu_item}")
        return {
            "message": "Menu item added successfully",
            "menu_item": menu_item
        }

    except Exception as e:
        print(f"Error adding menu item: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add menu item: {str(e)}"
        )