# admin.py
from typing import List
from app.models.models import Restaurant, MenuItem, User
from app.core.admin_middleware import get_current_admin
from app.dbConnection.mongoRepository import get_database
import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
import os
import shutil
from typing import Optional

db = get_database()
router = APIRouter(prefix="/restaurants")

UPLOAD_DIR = "static/restaurant_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=Restaurant)
async def create_restaurant(
        name: str = Form(...),
        cuisine_type: str = Form(...),
        rating: float = Form(...),
        address: str = Form(...),
        description: Optional[str] = Form(None),
        image: Optional[UploadFile] = File(None),
        current_admin: User = Depends(get_current_admin)
):
    try:
        print(f"Received restaurant creation request with image")

        # Validate data
        if not name or not cuisine_type:
            raise HTTPException(
                status_code=400,
                detail="Name and cuisine type are required"
            )

        # Create restaurant data
        restaurant_dict = {
            "id": str(uuid.uuid4()),
            "name": name,
            "cuisine_type": cuisine_type,
            "rating": float(rating),
            "address": address,
            "description": description or "",
            "created_by": str(current_admin.id),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "menu": []
        }

        # Handle image upload if provided
        if image:
            # Generate unique filename
            filename = f"{restaurant_dict['id']}_{image.filename}"
            file_path = os.path.join(UPLOAD_DIR, filename)

            # Save the image
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

            # Add image path to restaurant data
            restaurant_dict["image_url"] = f"/static/restaurant_images/{filename}"

            print(f"Saved image to {file_path}")

        # Insert into database
        result = db["restaurants"].insert_one(restaurant_dict)
        print(f"Insertion result: {result.inserted_id}")

        return restaurant_dict
    except Exception as e:
        print(f"Restaurant creation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Restaurant creation failed: {str(e)}"
        )

@router.put("/restaurants/{restaurant_id}", response_model=Restaurant)
async def update_restaurant(
        restaurant_id: str,
        restaurant_update: Restaurant,
        current_admin: User = Depends(get_current_admin)
):
    try:
        # Exclude id from update data
        update_data = restaurant_update.model_dump(exclude={'id'})
        update_data["updated_by"] = str(current_admin.id)
        update_data["updated_at"] = datetime.utcnow()

        result = db["restaurants"].update_one(
            {"id": restaurant_id},
            {"$set": update_data}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        updated_restaurant = db["restaurants"].find_one({"id": restaurant_id})
        if not updated_restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        return updated_restaurant
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/restaurants/{restaurant_id}")
async def delete_restaurant(
        restaurant_id: str,
        current_admin: User = Depends(get_current_admin)
):
    try:
        result = db["restaurants"].delete_one({"id": restaurant_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        return {"message": "Restaurant deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/restaurants/{restaurant_id}/menu", response_model=MenuItem)
async def add_menu_item(
        restaurant_id: str,
        menu_item: MenuItem,
        current_admin: User = Depends(get_current_admin)
):
    # Add more detailed logging
    print(f"Add Menu Item Request:")
    print(f"Restaurant ID: {restaurant_id}")
    print(f"Current User: {current_admin}")
    print(f"User ID: {current_admin.id}")
    print(f"User Email: {current_admin.email}")
    print(f"Is Admin: {current_admin.is_admin}")

    try:
        # First check if restaurant exists
        restaurant = db["restaurants"].find_one({"id": restaurant_id})
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")

        menu_item_dict = menu_item.model_dump()
        menu_item_dict["id"] = str(uuid.uuid4())

        result = db["restaurants"].update_one(
            {"id": restaurant_id},
            {
                "$push": {"menu": menu_item_dict},
                "$set": {
                    "updated_by": str(current_admin.id),
                    "updated_at": datetime.utcnow()
                }
            }
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Failed to add menu item")

        return menu_item_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/restaurants/{restaurant_id}/menu/{item_id}")
async def delete_menu_item(
        restaurant_id: str,
        item_id: str,
        current_admin: User = Depends(get_current_admin)
):
    try:
        logger.info(f"Attempting to delete menu item. Restaurant ID: {restaurant_id}, Item ID: {item_id}")

        # Find the restaurant first
        restaurant = db["restaurants"].find_one({"id": restaurant_id})
        if not restaurant:
            logger.error(f"Restaurant not found: {restaurant_id}")
            raise HTTPException(status_code=404, detail=f"Restaurant not found: {restaurant_id}")

        # Check if menu item exists
        menu_item = next((item for item in restaurant.get("menu", []) if item["id"] == item_id), None)
        if not menu_item:
            logger.error(f"Menu item not found. Restaurant ID: {restaurant_id}, Item ID: {item_id}")
            logger.error(f"Existing menu items: {restaurant.get('menu', [])}")
            raise HTTPException(status_code=404, detail=f"Menu item not found. Item ID: {item_id}")

        # Remove the menu item
        result = db["restaurants"].update_one(
            {"id": restaurant_id},
            {
                "$pull": {"menu": {"id": item_id}},
                "$set": {
                    "updated_by": str(current_admin.id),
                    "updated_at": datetime.utcnow()
                }
            }
        )

        if result.modified_count == 0:
            logger.error(f"Failed to delete menu item. Restaurant ID: {restaurant_id}, Item ID: {item_id}")
            raise HTTPException(status_code=404, detail="Failed to delete menu item")

        return {"message": "Menu item deleted successfully"}
    except Exception as e:
        logger.error(f"Unexpected error deleting menu item: {str(e)}")
        raise (HTTPException(status_code=500, detail=str(e))

               @router.put("/restaurants/{restaurant_id}/menu/{item_id}", response_model=Restaurant))
async def update_menu_item(
        restaurant_id: str,
        item_id: str,
        menu_item: MenuItem,
        current_admin: User = Depends(get_current_admin)
):
    try:
        menu_item_dict = menu_item.model_dump()
        menu_item_dict["id"] = item_id

        result = db["restaurants"].update_one(
            {
                "id": restaurant_id,
                "menu.id": item_id
            },
            {
                "$set": {
                    "menu.$": menu_item_dict,
                    "updated_by": str(current_admin.id),
                    "updated_at": datetime.utcnow()
                }
            }
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Restaurant or menu item not found")

        updated_restaurant = db["restaurants"].find_one({"id": restaurant_id})
        return updated_restaurant
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))