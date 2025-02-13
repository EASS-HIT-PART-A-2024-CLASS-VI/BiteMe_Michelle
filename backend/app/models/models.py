# app/models/models.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from enum import Enum

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
    id: str
    name: str
    cuisine_type: FoodCategory
    rating: float = Field(ge=0, le=5)
    address: str
    menu: List[MenuItem]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(from_attributes=True)

class OrderItem(BaseModel):
    menu_item_id: str
    restaurant_id: str
    name: str
    quantity: int = Field(gt=0, le=20)
    price: float = Field(gt=0)
    
    model_config = ConfigDict(from_attributes=True)

class Order(BaseModel):
    id: Optional[str] = None
    user_id: Optional[str] = None
    restaurant_id: str
    items: List[OrderItem]
    total_price: float = Field(gt=0)
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    special_instructions: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    id: Optional[str] = None
    is_active: bool = True
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