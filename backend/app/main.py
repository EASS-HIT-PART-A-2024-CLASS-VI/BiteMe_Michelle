from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Pydantic model for menu item
class MenuItem(BaseModel):
    name: str
    description: str
    price: float
    available: bool

menu = []  # Simple in-memory menu store

@app.get("/")
def read_root():
    return {"message": "Welcome to BiteMe!"}

@app.get("/menu", response_model=List[MenuItem])
def get_menu():
    return menu

@app.post("/menu")
def add_menu_item(item: MenuItem):
    menu.append(item)
    return {"message": "Item added successfully"}
