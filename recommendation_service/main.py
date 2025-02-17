import sys
import os

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from recommendation_service.models import SuggestedOrdersResponse
from .llm_integration import generate_recommendations
from .data_processing import get_user_past_orders, get_all_menu_items_with_restaurant
from .utils import get_current_time_of_day

# Import backend security
from backend.app.core.security import get_current_user
from backend.app.models.models import User

app = FastAPI(title="BiteMe Recommendation Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/suggest_orders", response_model=SuggestedOrdersResponse)
async def suggest_orders(current_user: User = Depends(get_current_user)):
    try:
        user_id = str(current_user.id)
        past_orders = get_user_past_orders(user_id)
        menu_items = get_all_menu_items_with_restaurant(user_id)
        time_of_day = get_current_time_of_day()

        suggestions = generate_recommendations(
            user_id, 
            past_orders, 
            menu_items, 
            time_of_day
        )

        if not suggestions:
            raise HTTPException(
                status_code=404, 
                detail="No recommendations could be generated"
            )

        return SuggestedOrdersResponse(
            user_id=int(user_id), 
            suggestions=suggestions
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error generating recommendations: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Recommendation Service"}