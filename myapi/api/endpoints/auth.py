
from fastapi import (
    APIRouter,
    Depends,
    status,
)

from fastapi.security import OAuth2PasswordBearer

from core.schemas import UserRequest
from app.models import AuthUser
from database.database import get_db
from core.securit import verify_password , save_hash_password

try:
    from sqlalchemy import insert,select , delete
    from sqlalchemy.ext.asyncio import AsyncSession
    
except ImportError:
    raise ImportError("Please install sqlachemy")



auth = APIRouter()


@auth.post(
    "/register",
    description="create access request for a user",
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    payload: UserRequest,
    db: AsyncSession = Depends(get_db)
) -> None:
    
    hashed = save_hash_password(payload.password)
        
    new_user = AuthUser(email=payload.email,password=hashed)
        
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return {"message" : "성공입니다"}


@auth.post(
    "/login",
    description="get token for a user"
)
async def login_user(
    payload: UserRequest,
    db: AsyncSession = Depends(get_db)
)-> None:
    
    return ""

