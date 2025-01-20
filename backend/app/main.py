<<<<<<< HEAD
from fastapi import FastAPI
from pydantic import BaseModel
=======
from fastapi import FastAPI, HTTPException
from app.mock import *
from app.models.types import *
from app.models.models import Order, MenuItem
from fastapi.middleware.cors import CORSMiddleware
import awkward as ak
>>>>>>> e37a76d (Updated backend with new features and fixed file tracking)
from typing import List

app = FastAPI()

<<<<<<< HEAD
# Pydantic model for menu item
class MenuItem(BaseModel):
    name: str
    description: str
    price: float
    available: bool
=======
# Define allowed origins for CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
>>>>>>> e37a76d (Updated backend with new features and fixed file tracking)

menu = []  # Simple in-memory menu store

@app.get("/")
def read_root():
<<<<<<< HEAD
    return {"message": "Welcome to BiteMe!"}

@app.get("/menu", response_model=List[MenuItem])
def get_menu():
=======
    """Welcome message and initial data."""
    restaurantTypesKeys = ak.Array([e.value for e in RestaurantType])
    restaurantTypesNames = ak.Array([e.name for e in RestaurantType])
    dishesResult = get_all_dishes()
    restaurantTypesResult = ak.zip({"index": restaurantTypesKeys, "name": restaurantTypesNames}).to_list()
    return {
        "message": "Welcome to BiteMe!",
        "restaurantTypes": restaurantTypesResult,
        "dishes": dishesResult,
    }

# Menu-related endpoints
@app.get("/menu", response_model=List[MenuItem])
def get_menu():
    """Get all menu items."""
>>>>>>> e37a76d (Updated backend with new features and fixed file tracking)
    return menu

@app.post("/menu")
def add_menu_item(item: MenuItem):
<<<<<<< HEAD
    menu.append(item)
    return {"message": "Item added successfully"}
=======
    """Add a new menu item."""
    menu.append(item)
    return {"message": "Item added successfully"}

# Restaurant-related endpoints
@app.get("/restaurants/get-by-city")
def get_restaurants_by_city(city: str):
    """Filter restaurants by city."""
    return get_restaurants_by_city(city)

@app.get("/restaurants/get-by-type")
def get_restaurants_by_type(restaurant_type: int):
    """Filter restaurants by type."""
    return get_restaurants_by_type(restaurant_type)

@app.get("/restaurants/get-by-dish")
def get_restaurants_by_dish(dish_name: str):
    """Filter restaurants by dish name."""
    return get_restaurants_by_dish(dish_name)

@app.post("/submit/place-order")
def place_order(order: Order):
    """Place a new order."""
    return {"message": "We successfully got your order!"}
>>>>>>> e37a76d (Updated backend with new features and fixed file tracking)
