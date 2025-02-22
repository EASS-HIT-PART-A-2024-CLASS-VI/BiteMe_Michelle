# app/main.py
import logging
from fastapi import FastAPI, HTTPException
from app.core.config import settings
from fastapi import File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os


# Configure logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Disable verbose logging for specific libraries
logging.getLogger("uvicorn").setLevel(logging.ERROR)
logging.getLogger("uvicorn.access").setLevel(logging.ERROR)
logging.getLogger("pymongo").setLevel(logging.ERROR)
logging.getLogger("motor").setLevel(logging.ERROR)

from app.core.config import settings
from app.dbConnection.mongoRepository import get_database

# Import routers
from app.api import orders, restaurants, users, admin

os.makedirs("static", exist_ok=True)
os.makedirs("static/restaurant_images", exist_ok=True)

app = FastAPI(
    title="BiteMe Food Delivery API",
    description="A comprehensive food delivery API",
    version="1.0.0"
)



# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get database instance
db = get_database()


# Mount static files
static_dir = os.path.abspath("static")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


# Include routers
app.include_router(orders.router, prefix="/orders", tags=["orders"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(restaurants.router, prefix="/restaurants", tags=["restaurants"])  # Fixed missing parenthesis

@app.get("/static/{path:path}")
async def read_static(path: str):
    print(f"Requested static path: {path}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Static directory exists: {os.path.exists('static')}")
    print(f"Full static path: {os.path.abspath('static')}")
    print(f"Requested file exists: {os.path.exists(os.path.join('static', path))}")
# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to BiteMe!"}

# Health check endpoint
@app.get("/health")
async def health_check():
    try:
        db.command("ping")
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )

# Startup event
@app.on_event("startup")
async def startup_event():
    logging.info("Application is starting up...")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Application is shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="error"  # Ensures only errors are logged
    )