from pydantic import BaseModel
from typing import List, Optional

class MenuItem(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    category: Optional[str] = None

class RecommendationRequest(BaseModel):
    restaurant_menu: List[MenuItem]
    user_previous_orders: Optional[List[str]] = []
    user_preference: Optional[str] = None  # New field for user's specific request

class Recommendation(BaseModel):
    recommended_items: List[str]
    reasoning: str