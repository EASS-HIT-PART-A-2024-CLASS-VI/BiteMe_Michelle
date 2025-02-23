import os
from datetime import datetime
from typing import List, Optional

import google.generativeai as genai
from dotenv import load_dotenv

from .models import MenuItem, Recommendation, RecommendationRequest, RecommendationAgent

load_dotenv()

def get_current_meal_time():
    hour = datetime.now().hour
    if 5 <= hour < 11:
        return "breakfast"
    elif 11 <= hour < 16:
        return "lunch"
    elif 16 <= hour < 22:
        return "dinner"
    else:
        return "late night"

class MenuRecommendationAgent(RecommendationAgent):
    def recommend(self, request: RecommendationRequest) -> Recommendation:
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("Gemini API key not found. Please check your .env file.")

        genai.configure(api_key=api_key)

        meal_time = get_current_meal_time()

        menu_text = "\n".join([
            f"- {item.name}: ${item.price:.2f} ({item.category or 'No category'}) - {item.description or 'No description'}"
            for item in request.restaurant_menu
        ])

        previous_orders_text = (
            f"Previously ordered items: {', '.join(request.user_previous_orders)}"
            if request.user_previous_orders
            else "No previous order history"
        )

        preference_text = f"User's specific preference: {request.user_preference}" if request.user_preference else ""

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
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)

            recommendation_text = response.text.strip()

            recommended_item = None
            for item in request.restaurant_menu:
                if item.name.lower() in recommendation_text.lower():
                    if item.description and item.description.lower() in recommendation_text.lower():
                        recommended_item = item.name
                        break
                    elif not recommended_item:
                        recommended_item = item.name

            if not recommended_item:
                recommended_item = request.restaurant_menu[0].name
                recommendation_text = f"Unable to find a perfect match. Suggesting {recommended_item} based on available options."

            recommendation = Recommendation(
                recommended_items=[recommended_item],
                reasoning=recommendation_text
            )
            return self.ai_validate(recommendation)

        except Exception as e:
            recommendation = Recommendation(
                recommended_items=[request.restaurant_menu[0].name],
                reasoning=f"AI recommendation failed. Recommending default item. Error: {str(e)}"
            )
            return self.ai_validate(recommendation)

async def generate_ai_recommendation(
        menu_items: List[MenuItem],
        previous_orders: Optional[List[str]] = None,
        user_preference: Optional[str] = None,
        is_authenticated: bool = False
) -> Recommendation:
    agent = MenuRecommendationAgent()
    request = RecommendationRequest(
        restaurant_menu=menu_items,
        user_previous_orders=previous_orders or [],
        user_preference=user_preference
    )
    return agent.recommend(request)