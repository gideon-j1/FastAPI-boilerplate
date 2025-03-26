
from fastapi import (
    APIRouter,
    Depends,
    status,
)

from core.schemas import UserRequest


try:
    from sqlalchemy import insert,select , delete
    from sqlalchemy.ext.asyncio import AsyncSession
    
except ImportError:
    raise ImportError("Please install sqlachemy")


book = APIRouter()



@book.post(
    "/register",
    description="create access token for request using user",
    status_code=status.HTTP_201_CREATED
)
async def login_token(
    new_user: UserRequest,   
    db: AsyncSession = Depends()
) -> None:
    
    
    print(new_user.email)
    
    
    return {"message" : "성공입니다"}

