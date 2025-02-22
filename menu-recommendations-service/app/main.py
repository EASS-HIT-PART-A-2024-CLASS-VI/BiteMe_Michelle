from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from .models import RecommendationRequest, Recommendation
from .utils import get_current_meal_time, create_recommendation_prompt, parse_recommendations

app = FastAPI(title="Menu Recommendation Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/recommend/", response_model=Recommendation)
async def get_recommendations(request: RecommendationRequest):
    try:
        meal_time = get_current_meal_time()
        menu_items = "\n".join([
            f"- {item.name}: ${item.price} - {item.description or 'No description'}"
            for item in request.restaurant_menu
        ])

        # Adapt prompt based on whether user has order history
        previous_orders = ""
        if request.user_previous_orders and len(request.user_previous_orders) > 0:
            previous_orders = "Previously ordered items: " + ", ".join(request.user_previous_orders)
            prompt = create_recommendation_prompt(menu_items, previous_orders, meal_time, has_history=True)
        else:
            prompt = create_recommendation_prompt(menu_items, "", meal_time, has_history=False)

        # Simple rule-based recommendations for demonstration
        # (You can replace this with Gemini AI later)
        recommended_items = []
        reasoning_parts = []

        # If no previous orders, focus on popular/signature items
        if not request.user_previous_orders:
            # Try to find items from different categories
            categories = {"Main": False, "Salads": False, "Dessert": False}
            
            for item in request.restaurant_menu:
                if len(recommended_items) >= 3:
                    break
                    
                category = item.category or "Other"
                if not categories.get(category, False):
                    recommended_items.append(item.name)
                    if meal_time == "dinner" and category == "Main":
                        reasoning_parts.append(f"{item.name}: A perfect dinner option with {item.description}")
                    elif category == "Salads":
                        reasoning_parts.append(f"{item.name}: A fresh and healthy choice")
                    elif category == "Dessert":
                        reasoning_parts.append(f"{item.name}: A delightful way to end your meal")
                    else:
                        reasoning_parts.append(f"{item.name}: A tasty choice from our menu")
                    categories[category] = True

        else:
            # Include one previous order and two new items
            # First, add one familiar item
            familiar_item = request.user_previous_orders[0]
            recommended_items.append(familiar_item)
            reasoning_parts.append(f"{familiar_item}: One of your favorites from previous orders")

            # Add two new items from different categories
            new_items = [item for item in request.restaurant_menu 
                        if item.name not in request.user_previous_orders]
            for item in new_items[:2]:
                recommended_items.append(item.name)
                reasoning_parts.append(f"{item.name}: A new dish we think you'll enjoy based on your preferences")

        # Fill remaining slots if needed
        while len(recommended_items) < 3:
            for item in request.restaurant_menu:
                if item.name not in recommended_items:
                    recommended_items.append(item.name)
                    reasoning_parts.append(f"{item.name}: A popular choice from our menu")
                    break

        # Create final reasoning text
        reasoning = "\n".join(reasoning_parts) + "\n\nThese items provide a good variety for your " + meal_time + " meal."

        return Recommendation(
            recommended_items=recommended_items[:3],  # Ensure only 3 items
            reasoning=reasoning
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}