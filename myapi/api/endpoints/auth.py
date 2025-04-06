
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
from database.database import redis_client

from core.securit import save_hash_password
from core.jwt import create_token
from core.redis import add_redis_item


try:
    from sqlalchemy import insert,select , delete
    from sqlalchemy.ext.asyncio import AsyncSession
    from datetime import datetime, timedelta, timezone
    
except ImportError:
    raise ImportError("Please install sqlachemy or import datetime")


from datetime import date,datetime,timezone,timedelta
import uuid

auth = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30 # 5 hour
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
        
    user_ud = str(uuid.uuid4())[:8]
        
    access_token = create_token(
        data={
            "id" : user_ud,
            "iss": "username",
        },
        expires_delta=access_token_expires
    )
    
    print(access_token)
    
    refresh_token = create_token(
        data={
            "id" : user_ud,
            "iss" : "username",
        },
        expires_delta=refresh_token_expires
    )
    
    exp = str(access_token.expires_at.timestamp()).split(".")[0]
    n_exp = int(exp)
    
    token ={
        "id" : access_token.id,
        "access" : access_token.access_token,
        "exp" : n_exp,
        "refresh" : refresh_token.refresh_token
    }

    add_redis_item(token)
    
    return {
        "access": f"{access_token.access_token}",
        "refresh": f"{refresh_token.refresh_token}"
    }

import time
from typing import Dict,Any
import json

r"""
 token ={
     "id" : "1f321321",
     "exp" : 13213,
     "token access" : ey321321321flk.jadsfojdsahfkjl~
 }
"""

@auth.get("/get_redis")
async def get_refresh_token(token: Dict[Any,Any] = None)->None:
    
    token_list = redis_client.lrange("mytoken",0,100)    
        

    
    r"""
        들어오는 토큰에 id가 현재 redis list에서 가져온 id와 동일한지 검사
        -> redis key에 저장된 exp값과 현재 시간 검사
        
        -> yse (토큰 유효기간이 아직 남아있음)
        -> no (새로운 토큰 발급하고 redis에 새로운 토큰으로 교체하고 토큰 발급)
    """
    
    user_id = "9b755e04" 
    
    cur_time = int(time.time())
    for t in token_list:
        json_str = t.decode()
        
        token_data = json.loads(json_str)
                
        if token_data["id"] == user_id:
            if 1743922031 < cur_time:
                access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
                access_token = create_token(
                    data={
                        "id" : user_id,
                        "iss": "username",
                    },
                    expires_delta=access_token_expires
                )
                
                for idx,t2 in enumerate(token_list):
             
                        jsont_str2 = t2.decode()
                        
                        token_data2 = json.loads(jsont_str2)
                        
                        
                        if token_data2["id"] == user_id:
                            
                            redis_payload = {
                                "id" : user_id,
                                "key" : token_data2["key"],
                                "access" : access_token.access_token,
                                "refresh" : token_data2["refresh"],
                            }
                            
                            redis_client.lset("mytoken",idx,json.dumps(redis_payload))
                            
                            return {
                                "mesaage" : "creat new access token",
                                "token" : f"{access_token.access_token}"
                            } 
                                
            else:
               raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="expire time is valid.") 
            
                
        
    
