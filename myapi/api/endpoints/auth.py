
from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException
)


from core.schemas import UserRequest
from app.models import AuthUser
from database.database import get_db

from core.securit import create_access_token ,save_hash_password

try:
    from sqlalchemy import insert,select , delete
    from sqlalchemy.ext.asyncio import AsyncSession
    from datetime import datetime, timedelta, timezone
    
except ImportError:
    raise ImportError("Please install sqlachemy or import datetime")



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



from core.securit import SECRET_KEY , ACCESS_TOKEN_EXPIRE_MINUTES

r"""
    [] : 이메일 중복으로 로그인 할시 에러처리하기
    [] : 비밀번호 틀려도 토큰 발급 되고 있음
"""

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

    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found please create user"
        )
            
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    print(access_token_expires)
    
    access_token = create_access_token(data={"sub" : "test_user"},expires_delta=access_token_expires)
    

    return {"message" : f"성공입니다. Token : {access_token}"}

