from pydantic import BaseModel
from typing import List
from app.models.types import RestaurantType

class MenuItem(BaseModel):
    name: str
    description: str
    price: float
    available: bool

class Restaurant(BaseModel):
    id: int
    name: str
    type: RestaurantType
    city: str
    menu: List[MenuItem]

class Order(BaseModel):
    restaurant_id: int
    dish_name: str
    quantity: int
    customer_name: str
