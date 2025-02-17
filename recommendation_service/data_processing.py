import requests
import os
from typing import List, Dict
from dotenv import load_dotenv
from recommendation_service.models import SuggestedDish

# Load environment variables
load_dotenv()

# Get BACKEND_API_URL from environment variable
BACKEND_API_URL = os.getenv("BACKEND_API_URL")

if BACKEND_API_URL is None:
    raise ValueError("BACKEND_API_URL environment variable must be set.")

def get_access_token():
    try:
        username = os.getenv("BACKEND_USERNAME")
        password = os.getenv("BACKEND_PASSWORD")

        if not username or not password:
            raise ValueError("BACKEND_USERNAME and BACKEND_PASSWORD must be set")

        # Construct token endpoint
        token_endpoint = f"{BACKEND_API_URL}/users/token"

        # Create form data
        form_data = {
            "username": username,
            "password": password
        }

        # Send token request
        response = requests.post(token_endpoint, data=form_data)
        response.raise_for_status()

        # Extract access token
        token_data = response.json()
        return token_data.get("access_token")

    except Exception as e:
        print(f"Error getting access token: {e}")
        return None

def get_user_past_orders(user_id: str) -> List[dict]:
    # Get access token
    access_token = get_access_token()
    if not access_token:
        print("Failed to obtain access token")
        return []

    try:
        # Construct orders endpoint
        orders_endpoint = f"{BACKEND_API_URL}/users/me/orders"
        
        # Send request with access token
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(orders_endpoint, headers=headers)
        response.raise_for_status()

        # Return orders
        return response.json()

    except Exception as e:
        print(f"Error fetching past orders: {e}")
        return []

def get_all_menu_items_with_restaurant(user_id: str) -> List[dict]:
    # Get access token
    access_token = get_access_token()
    if not access_token:
        print("Failed to obtain access token")
        return []

    try:
        # Get past orders to get restaurant IDs
        past_orders = get_user_past_orders(user_id)
        
        # Extract unique restaurant IDs
        restaurant_ids = set(order.get('restaurant_id') for order in past_orders if order.get('restaurant_id'))
        
        # Fetch menu items for each restaurant
        all_menu_items = []
        headers = {"Authorization": f"Bearer {access_token}"}

        for restaurant_id in restaurant_ids:
            restaurant_endpoint = f"{BACKEND_API_URL}/restaurants/{restaurant_id}"
            response = requests.get(restaurant_endpoint, headers=headers)
            response.raise_for_status()
            
            restaurant = response.json()
            
            # Add restaurant context to menu items
            for item in restaurant.get('menu', []):
                menu_item = {
                    **item,
                    "restaurant_name": restaurant.get('name'),
                    "restaurant_id": restaurant_id
                }
                all_menu_items.append(menu_item)

        return all_menu_items

    except Exception as e:
        print(f"Error fetching menu items: {e}")
        return []