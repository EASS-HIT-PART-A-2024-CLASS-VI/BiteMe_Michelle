from pydantic import BaseModel, Field
from typing import List, Optional
import pydantic_ai

class MenuItem(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    category: Optional[str] = None

class RecommendationRequest(BaseModel):
    restaurant_menu: List[MenuItem]
    user_previous_orders: Optional[List[str]] = []
    user_preference: Optional[str] = None

class Recommendation(BaseModel):
    recommended_items: List[str] = Field(default_factory=list)
    reasoning: str = Field(default="")

class RecommendationAgent(pydantic_ai.Agent):
    def recommend(self, request: RecommendationRequest) -> Recommendation:
        # This method will be implemented in utils.py
        pass

    def ai_validate(self, recommendation: Recommendation) -> Recommendation:
        if not recommendation.recommended_items:
            recommendation.recommended_items = ["Default item"]
            recommendation.reasoning = "No recommendations found. Providing a default item."
        elif len(recommendation.recommended_items) > 3:
            recommendation.recommended_items = recommendation.recommended_items[:3]
            recommendation.reasoning += " (Limited to top 3 recommendations)"
        return recommendation