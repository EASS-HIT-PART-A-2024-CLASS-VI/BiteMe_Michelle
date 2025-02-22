from pydantic import BaseModel, EmailStr, Field, ConfigDict, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum
import re
from fastapi import File, UploadFile, Form

class FoodCategory(str, Enum):
    ITALIAN = "Italian"
    JAPANESE = "Japanese"
    MEXICAN = "Mexican"
    INDIAN = "Indian"
    AMERICAN = "American"
    CHINESE = "Chinese"

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    READY = "READY"
    IN_DELIVERY = "IN_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class MenuItem(BaseModel):
    name: str
    description: str
    price: float = Field(gt=0)
    category: FoodCategory
    spiciness_level: Optional[int] = Field(None, ge=1, le=5)
    is_vegetarian: bool = False
    available: bool = True

    model_config = ConfigDict(from_attributes=True)

class Restaurant(BaseModel):
    id: Optional[str] = None
    name: str
    cuisine_type: FoodCategory
    rating: float = Field(ge=0, le=5)
    address: str
    description: Optional[str] = None
    menu: List[MenuItem] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra='ignore'  # Ignore extra fields
    )

# 🚨 **FIX: Move OrderItem outside Restaurant class**
class OrderItem(BaseModel):
    menu_item_id: str
    restaurant_id: str
    name: str
    quantity: int = Field(gt=0, le=20)
    price: float = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)

    @validator('quantity')
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v

class Order(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    restaurant_id: Optional[str] = None
    items: List[OrderItem]
    total_price: float = Field(gt=0)
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    special_instructions: Optional[str] = None
    payment_method: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @validator('total_price')
    def validate_total_price(cls, v):
        if v <= 0:
            raise ValueError('Total price must be positive')
        return v

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    id: Optional[str] = None
    is_active: bool = True
    is_admin: bool = False  # New field for admin status
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(from_attributes=True)

class TokenData(BaseModel):
    email: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class RestaurantFilter(BaseModel):
    cuisine_type: Optional[FoodCategory] = None
    min_rating: Optional[float] = Field(None, ge=0, le=5)
    is_vegetarian_friendly: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

class ReviewCreate(BaseModel):
    restaurant_id: str
    rating: float = Field(ge=1, le=5)
    comment: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class Review(ReviewCreate):
    id: str
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)