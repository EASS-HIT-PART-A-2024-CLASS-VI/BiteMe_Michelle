from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import RecommendationRequest, Recommendation
from .utils import generate_ai_recommendation

# Create FastAPI app
app = FastAPI(
    title="AI Menu Recommendation Service",
    description="Intelligent, interactive menu recommendation microservice"
)

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
    """
    Generate personalized menu recommendation.

    Args:
        request: Contains restaurant menu, user's previous orders, and optional preference

    Returns:
        Structured recommendation
    """
    try:
        # Generate recommendation using custom logic
        recommendation = generate_ai_recommendation(
            menu_items=request.restaurant_menu,
            previous_orders=request.user_previous_orders,
            user_preference=request.user_preference
        )

        return recommendation

    except Exception as e:
        # Proper error handling
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendation: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "service": "Menu Recommendations"}