import os
import json
from typing import List
import openai
from dotenv import load_dotenv
from recommendation_service.models import SuggestedDish

# Load environment variables
load_dotenv()

# Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_recommendations(user_id: str, past_orders: List[dict], all_menu_items: List[dict], time_of_day: str) -> List[SuggestedDish]:
    """Generates personalized food recommendations using OpenAI."""
    
    # Limit the input data to prevent token overflow
    past_orders = past_orders[:10]  # Limit to last 10 orders
    all_menu_items = all_menu_items[:50]  # Limit to 50 menu items

    prompt = f"""
    You are a food recommendation expert for the BiteMe app. Analyze the following user data:

    User ID: {user_id}
    Time of Day: {time_of_day}
    Past Orders: {json.dumps(past_orders)}
    Available Menu Items: {json.dumps(all_menu_items)}

    Provide 3 personalized dish recommendations based on:
    1. User's order history
    2. Time of day
    3. Variety and culinary diversity

    For each recommendation, include:
    - dish_name
    - restaurant_name
    - description
    - cuisine
    - price
    - reason for recommendation
    - image_url (optional)

    Return ONLY a valid JSON array of recommendation objects.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful food recommendation assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7,
        )

        raw_suggestions = response.choices[0].message.content.strip()

        try:
            suggestions_json = json.loads(raw_suggestions)
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e}")
            print(f"Raw LLM Response: {raw_suggestions}")
            return []

        suggestions: List[SuggestedDish] = [SuggestedDish(**suggestion) for suggestion in suggestions_json]
        return suggestions

    except Exception as e:
        print(f"Recommendation generation error: {e}")
        return []