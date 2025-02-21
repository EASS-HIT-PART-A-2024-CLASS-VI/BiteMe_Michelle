from fastapi import HTTPException, Depends
from app.core.security import get_current_user
from app.models.models import User

async def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to access this resource"
        )
    return current_user