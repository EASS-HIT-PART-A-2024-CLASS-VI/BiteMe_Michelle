from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from bson import ObjectId

from app.core.security import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    get_current_user
)
from app.models.models import User, UserCreate, UserUpdate, Token
from app.dbConnection.mongoRepository import get_database
from app.core.config import settings

router = APIRouter()
db = get_database()

@router.post("/register", response_model=User)
async def register_user(user_data: UserCreate):
    # Check if user exists
    if db["users"].find_one({"email": user_data.email}):
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    user_dict = user_data.model_dump()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    user_dict["is_active"] = True
    
    result = db["users"].insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    
    return User(**user_dict)

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Find user
    user = db["users"].find_one({"email": form_data.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
@router.put("/me", response_model=User)
async def update_user_profile(
        user_update: UserUpdate,
        current_user: User = Depends(get_current_user)
):
    try:
        # Debug prints
        print("Current user object:", current_user)
        print("Current user ID type:", type(current_user.id))
        print("Current user ID:", current_user.id)

        # Ensure we have a valid user ID
        if not current_user.id:
            raise HTTPException(
                status_code=401,
                detail="Authentication failed: No user ID found"
            )

        # Prepare update data
        update_data = {}

        # Update full name if provided
        if user_update.full_name:
            update_data["full_name"] = user_update.full_name

        # Update phone number if provided
        if user_update.phone_number:
            update_data["phone_number"] = user_update.phone_number

        # Update password if provided
        if user_update.password:
            update_data["hashed_password"] = get_password_hash(user_update.password)

        # Check if there's anything to update
        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="No update data provided"
            )

        # Ensure we're using the correct ID type for MongoDB
        try:
            user_id = ObjectId(current_user.id)
        except Exception as e:
            print(f"Error converting user ID: {e}")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid user ID: {current_user.id}"
            )

        # Perform the update
        result = db["users"].update_one(
            {"_id": user_id},
            {"$set": update_data}
        )

        # Check if update was successful
        if result.modified_count == 0:
            # Try to find the user to understand why
            existing_user = db["users"].find_one({"_id": user_id})
            if not existing_user:
                raise HTTPException(
                    status_code=404,
                    detail="User not found in database"
                )

            # If user exists but no update, it might mean no changes were made
            raise HTTPException(
                status_code=400,
                detail="No changes were made. The new data might be identical to existing data."
            )

        # Fetch the updated user
        updated_user = db["users"].find_one({"_id": user_id})

        if not updated_user:
            raise HTTPException(
                status_code=404,
                detail="User not found after update"
            )

        # Convert ObjectId to string
        updated_user['id'] = str(updated_user['_id'])

        return User(**updated_user)

    except Exception as e:
        # Log the full error for debugging
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Error updating profile: {str(e)}"
        )

@router.get("/me/orders")
async def read_user_orders(current_user: User = Depends(get_current_user)):
    orders = list(db["orders"].find({"user_id": str(current_user.id)}))
    return orders