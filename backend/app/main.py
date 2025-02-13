# app/main.py
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Optional
from datetime import timedelta
from bson import ObjectId

from app.core.config import settings
from app.core.security import create_access_token, get_current_user, get_password_hash
from app.models.models import (
    Restaurant,  # Ensure this is imported
    MenuItem, 
    FoodCategory,
    User, 
    UserCreate, 
    Token, 
    Order, 
    OrderStatus
)
from app.dbConnection.mongoRepository import get_database

# Import routers
from app.api import orders, restaurants, users

app = FastAPI(title="BiteMe Food Delivery API")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get database instance
db = get_database()

# Include routers
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(restaurants.router, prefix="/restaurants", tags=["restaurants"])
app.include_router(users.router, prefix="/users", tags=["users"])

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to BiteMe!"}

# Authentication endpoints and other existing endpoints remain the same as in your previous implementation

# Health check endpoint
@app.get("/health")
async def health_check():
    try:
        db.command('ping')
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)