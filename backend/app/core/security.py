# app/core/security.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from bson import ObjectId

from app.core.config import settings
from app.models.models import User, TokenData
from app.dbConnection.mongoRepository import get_database

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password

    Args:
        plain_password (str): The plain text password to verify
        hashed_password (str): The hashed password to compare against

    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a plain text password

    Args:
        password (str): The plain text password to hash

    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token

    Args:
        data (dict): The data to encode in the token
        expires_delta (Optional[timedelta]): Token expiration time

    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()

    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    # Encode and return the token
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get the current authenticated user from a JWT token

    Args:
        token (str): The JWT token

    Returns:
        User: The authenticated user

    Raises:
        HTTPException: If credentials cannot be validated
    """
    # Exception for unauthorized access
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        # Extract email from token
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        # Create token data
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    # Get database connection
    db = get_database()

    # Find user by email
    user = db["users"].find_one({"email": token_data.email})
    if user is None:
        raise credentials_exception

    # Normalize user data
    user_dict = {
        **user,
        "id": str(user['_id']),  # Convert ObjectId to string
        "is_admin": user.get('is_admin', False)  # Ensure is_admin exists
    }

    return User(**user_dict)

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current active user

    Args:
        current_user (User): The authenticated user

    Returns:
        User: The active user

    Raises:
        HTTPException: If the user is not active
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Get the current admin user

    Args:
        current_user (User): The authenticated user

    Returns:
        User: The admin user

    Raises:
        HTTPException: If the user is not an admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this resource"
        )
    return current_user