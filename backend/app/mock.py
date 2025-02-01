from typing import List

# Mock data for restaurants
restaurants = [
    {
        "name": "Pizza Paradise",
        "city": "Tel Aviv",
        "menu": [
            {"name": "Margherita", "description": "Classic pizza", "price": 10.0, "available": True},
            {"name": "Pepperoni", "description": "Spicy pepperoni pizza", "price": 12.0, "available": True}
        ]
    },
    {
        "name": "Sushi World",
        "city": "Haifa",
        "menu": [
            {"name": "California Roll", "description": "Crab and avocado roll", "price": 8.0, "available": True},
            {"name": "Salmon Nigiri", "description": "Fresh salmon on rice", "price": 10.0, "available": False}
        ]
    },
    {
        "name": "Burger World",
        "city": "New York",
        "menu": [
            {"name": "Classic Burger", "description": "A delicious classic beef burger", "price": 9.99, "available": True},
            {"name": "Cheese Burger", "description": "A beef burger with melted cheese", "price": 11.99, "available": True},
            {"name": "Fries", "description": "Crispy golden fries", "price": 4.99, "available": True}
        ]
    }
]

# Mock functions for testing
def get_all_restaurants():
    return restaurants

def get_restaurants_by_city(city: str):
    return [r for r in restaurants if r["city"].lower() == city.lower()]

def get_restaurants_by_dish(dish_name: str):
    return [
        r for r in restaurants if any(dish["name"].lower() == dish_name.lower() for dish in r["menu"])
    ]

def get_restaurant_by_name(name: str):
    for r in restaurants:
        if r["name"].lower() == name.lower():
            return r
    return None
