from app.models.models import Restaurant, MenuItem
from app.models.types import RestaurantType

restaurants = [
    Restaurant(
        id=1,
        name="Pizza Paradise",
        type=RestaurantType.ITALIAN,
        city="Tel Aviv",
        menu=[
            MenuItem(name="Margherita", description="Classic pizza", price=10.0, available=True),
            MenuItem(name="Pepperoni", description="Spicy pepperoni pizza", price=12.0, available=True),
        ],
    ),
    Restaurant(
        id=2,
        name="Sushi World",
        type=RestaurantType.JAPANESE,
        city="Haifa",
        menu=[
            MenuItem(name="California Roll", description="Crab and avocado roll", price=8.0, available=True),
            MenuItem(name="Salmon Nigiri", description="Fresh salmon on rice", price=10.0, available=False),
        ],
    ),
]

def get_all_dishes():
    return [item.name for restaurant in restaurants for item in restaurant.menu]

def get_restaurants_by_city(city: str):
    return [r.dict() for r in restaurants if r.city.lower() == city.lower()]

def get_restaurants_by_type(restaurant_type: int):
    return [r.dict() for r in restaurants if r.type.value == restaurant_type]

def get_restaurants_by_dish(dish_name: str):
    return [r.dict() for r in restaurants if any(d.name.lower() == dish_name.lower() for d in r.menu)]
