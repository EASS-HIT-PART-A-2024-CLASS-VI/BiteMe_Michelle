from pydantic import BaseModel, Field
from typing import List, Optional

class SuggestedDish(BaseModel):
    dish_name: str = Field(..., description="Name of the suggested dish")
    restaurant_name: str = Field(..., description="Name of the restaurant")
    description: str = Field(..., description="Description of the dish")
    cuisine: str = Field(..., description="Cuisine type")
    price: float = Field(..., description="Price of the dish")
    image_url: Optional[str] = Field(None, description="URL of the dish image")
    reason: str = Field(..., description="Reason for the suggestion")

class SuggestedOrdersResponse(BaseModel):
    user_id: int = Field(..., description="ID of the user")
    suggestions: List[SuggestedDish]