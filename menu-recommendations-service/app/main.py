from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .models import RecommendationRequest, Recommendation
from .utils import generate_ai_recommendation

app = FastAPI(
    title="AI Menu Recommendation Service",
    description="Intelligent, interactive menu recommendation microservice"
)

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
        recommendation = await generate_ai_recommendation(
            menu_items=request.restaurant_menu,
            previous_orders=request.user_previous_orders,
            user_preference=request.user_preference
        )
        return recommendation
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendation: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Menu Recommendations"}