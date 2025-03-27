from pydantic import BaseModel,ConfigDict,EmailStr
from datetime import datetime
from typing import Optional

###############  Book ################
class BookRequest(BaseModel):
    description: str
    price: int

class BookResponse(BookRequest):
    id: int

    
    r"""
        Pydantic v1
        ORM 객체 -> DTO 변환 역할
        
        DTO: DB에서 가져온 ORM 객체를 API에 사용할 수 있게 변환
    """
    
    class Config:
        from_attributes = True
        

############### Auth ################
class UserRequest(BaseModel):
    email: EmailStr
    password: str
    


class BaseResquest(UserRequest):
    r"""
        Pydantic v2 
    """
    id: int   
    model_config = ConfigDict(from_attributes=True)



class Token(BaseModel):
    access_token: str
    expires_at: datetime
    refresh_token: str
    refresh_token_expires_at: datetime

