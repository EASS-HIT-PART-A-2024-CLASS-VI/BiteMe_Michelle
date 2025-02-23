import os
from datetime import datetime
from typing import List, Optional

import google.generativeai as genai
from dotenv import load_dotenv

from .models import MenuItem, Recommendation

# Load environment variables
load_dotenv()

def get_current_meal_time():
    """Determine the meal time based on current hour"""
    hour = datetime.now().hour
    if 5 <= hour < 11:
        return "breakfast"
    elif 11 <= hour < 16:
        return "lunch"
    elif 16 <= hour < 22:
        return "dinner"
    else:
        return "late night"

def generate_ai_recommendation(
        menu_items: List[MenuItem],
        previous_orders: Optional[List[str]] = None,
        user_preference: Optional[str] = None,
        is_authenticated: bool = False
) -> Recommendation:
    # Get Gemini API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("Gemini API key not found. Please check your .env file.")

    # Configure Gemini API
    genai.configure(api_key=api_key)

    # Get current meal time
    meal_time = get_current_meal_time()

    # Prepare menu items text
    menu_text = "\n".join([
        f"- {item.name}: ${item.price:.2f} ({item.category or 'No category'}) - {item.description or 'No description'}"
        for item in menu_items
    ])

    # Prepare previous orders text
    previous_orders_text = (
        f"Previously ordered items: {', '.join(previous_orders)}"
        if previous_orders and len(previous_orders) > 0
        else "No previous order history"
    )

    # Prepare user preference text
    preference_text = f"User's specific preference: {user_preference}" if user_preference else ""

    # Create a detailed prompt for Gemini
    prompt = f"""
    You are an expert restaurant recommendation AI for {meal_time}. 
    Help find the perfect menu item based on the following context:

    Available Menu Items:
    {menu_text}

    {previous_orders_text}

    {preference_text}

    Recommendation Guidelines:
    1. Current meal time is {meal_time}
    2. If user specified a preference, prioritize matching that preference
    3. Consider menu items, their descriptions, and categories
    4. ONLY recommend an item that EXACTLY matches a name in the available menu items
    5. Provide a clear, personalized reasoning for the recommendation

    Your response MUST include:
    - EXACT name of ONE menu item from the available menu
    - A brief, compelling explanation of why this item is recommended
    - If no perfect match is found, suggest the closest alternative
    """

    try:
        # Use Gemini to generate recommendation
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)

        # Parse the response
        recommendation_text = response.text.strip()

        # Validate the recommendation is for an existing menu item
        recommended_item = None
        for item in menu_items:
            if item.name.lower() in recommendation_text.lower():
                recommended_item = item.name
                break

        # Fallback if no valid item found
        if not recommended_item:
            recommended_item = menu_items[0].name
            recommendation_text = f"Unable to find a perfect match. Suggesting {recommended_item} based on available options."

        return Recommendation(
            recommended_items=[recommended_item],
            reasoning=recommendation_text
        )

    except Exception as e:
        # Fallback recommendation
        return Recommendation(
            recommended_items=[menu_items[0].name],
            reasoning=f"AI recommendation failed. Recommending default item. Error: {str(e)}"
        )