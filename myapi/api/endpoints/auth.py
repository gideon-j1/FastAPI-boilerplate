
from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException
)

from core.securit import verify_password
from core.schemas import UserRequest
from app.models import AuthUser
from database.database import get_db

from core.securit import save_hash_password
from core.jwt import create_token


try:
    from sqlalchemy import insert,select , delete
    from sqlalchemy.ext.asyncio import AsyncSession
    from datetime import datetime, timedelta, timezone
    
except ImportError:
    raise ImportError("Please install sqlachemy or import datetime")



auth = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 1 # 5 hour
REFRESH_TOKEN_EXPIRE_MINUTES = 28 * 24 * 60 # 28 day

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

    if payload.password == "" or payload.email== "":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="empty value (email,password)"
        )
    
    stmt = select(AuthUser).where(AuthUser.email == payload.email)
    
    query = await db.execute(stmt)
    
    user = query.scalars().first()

    hashed = verify_password(payload.password , user.password)
        
    if not hashed:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="user password is wrong"
        )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found please create user"
        )
            
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        
    access_token = create_token(
        data={
            "iss": "username",
        },
        expires_delta=access_token_expires
    )
    
    refresh_token = create_token(
        data={
            "iss" : "username",
        },
        expires_delta=refresh_token_expires
    )
    
    return {
        "access": f"{access_token.access_token}",
        "refresh": f"{refresh_token.refresh_token}"
    }

    
    

from database.database import redis_client
from core.schemas import Token
from typing import Dict,Any

@auth.post("/redis")
async def add_redis_item(
    token: Dict[Any,Any] = None) -> None:
    
    # test token
    # payload = {
    # "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VybmFtZSIsImV4cCI6MTc0MzU5NTI2MiwiaWF0IjoxNzQzNTk1MjAyfQ.miY2Dq5R-OIpKcJORuzcASWLiyslf73FwSp2SmWvlOCQ",
    # "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VybmFtZSIsImV4cCI6MTc0NjAxNDQwMiwiaWF0IjoxNzQzNTk1MjAyfQ.oIy3qgV9682N9JOJnQvV7VriEHo7nAa-DMGihNssi92k"
    # }
    
    item = redis_client.set(f"{token["access"]}" , f"{token["refresh"]}")
    
    return {"message" : "성공입니다."}


import jwt 
import bcrypt
from core.securit import SECRET_KEY,ALGORITHM


@auth.get("/get_redis")
async def get_refresh_token()->None:
    
    item = redis_client.get("token")    
    
    time = str(datetime.now(timezone.utc) + timedelta(minutes=1))
    
    t = time.split()
    
    year_t = t[0].split('-')
    
    y1 = int(year_t[0])
    month = int(year_t[1])
    day = int(year_t[2])
    
    total_y = y1+month+day
    
    current_timer = t[1].split(':')

    hour = int(current_timer[0])
    minute = int(current_timer[1])
    second = int(current_timer[2].split('.')[0])

    total_h = hour+minute+second
    
    cur_time_total = total_h + total_y

    f_t = str(datetime.fromtimestamp(1743513559)).split()
    
    year_f = f_t[0].split('-')
    
    y_f_1 = int(year_f[0])
    y_f_2 = int(year_f[1])
    y_f_3 = int(year_f[2])
    
    total_y_f = y_f_1 + y_f_2 + y_f_3
    
    current_timer_f_t = f_t[1].split(':')
    
    hour_y_f = int(current_timer_f_t[0])
    minute_y_f = int(current_timer_f_t[1])
    second_y_f = int(current_timer_f_t[2].split('.')[0])
    
    total_y_f2 = hour_y_f + minute_y_f + second_y_f
    
    redis_total = total_y_f + total_y_f2
    
    if cur_time_total < redis_total:
        raise Exception("cache token are larger! ")
    
    new_token = item
    
    if (type(new_token) is not bytes):
        raise Exception("not token type")
        
    
    
    return {
        "message" : "성공입니다",
        "item" : f"{item.decode("utf-8")}"
    }
    
