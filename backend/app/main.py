from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional, Union
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.dbConnection.mongoRepository import get_database
from app.models.models import Restaurant

# FastAPI instance
app = FastAPI()

# Define allowed origins for CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database instance
db = get_database()

# Authentication configuration
SECRET_KEY = "your_secret_key"  # Replace with a secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fake database for authentication
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": pwd_context.hash("password"),
        "disabled": False,
    }
}

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

# Helper functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db: Dict[str, Dict], username: str) -> Optional[UserInDB]:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None

def authenticate_user(db: Dict[str, Dict], username: str, password: str) -> Union[UserInDB, bool]:
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Routes
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = get_user(fake_users_db, username=username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/")
def read_root():
    return {"message": "Welcome to BiteMe!"}

@app.get("/restaurants")
def get_all_restaurants():
    """
    Fetch all restaurants from the database.
    """
    try:
        restaurants = db["restaurants"].find({}, {"_id": 0})  # Exclude MongoDB's _id field
        return {"success": True, "restaurants": list(restaurants)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/restaurants/get-by-city")
def get_restaurants_by_city(city: str):
    """
    Fetch restaurants in a specific city.
    """
    try:
        restaurants = db["restaurants"].find({"city": city}, {"_id": 0})  # Match by city
        restaurant_list = list(restaurants)
        if not restaurant_list:
            raise HTTPException(status_code=404, detail="No restaurants found in this city.")
        return {"success": True, "restaurants": restaurant_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/restaurants/get-by-dish")
def get_restaurants_by_dish(dish_name: str):
    """
    Fetch restaurants that serve a specific dish.
    """
    try:
        restaurants = db["restaurants"].find(
            {"menu.name": dish_name}, {"_id": 0}
        )  # Query menu items inside restaurants
        restaurant_list = list(restaurants)
        if not restaurant_list:
            raise HTTPException(status_code=404, detail="No restaurants serve this dish.")
        return {"success": True, "restaurants": restaurant_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/restaurants/get-by-name")
def get_restaurants_by_name(name: str):
    """
    Fetch a restaurant by its name.
    """
    try:
        restaurant = db["restaurants"].find_one({"name": name}, {"_id": 0})
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        return {"success": True, "restaurant": restaurant}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
