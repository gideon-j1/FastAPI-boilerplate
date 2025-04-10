from pydantic import BaseModel,ConfigDict,EmailStr
from datetime import datetime
from typing import Set,List

# tuple 전용 basemodel
class MyBaseModel(BaseModel):
    def __hash__(self):
        return hash((type(self),) ) + tuple(self.__dict__.values())

###############  Book ################


class NewBookResponse(BaseModel):
    tableoid: str
    id: int
    description: str
    price: int
    
class PartitionResponse(BaseModel):
    first: List[NewBookResponse]
    second: List[NewBookResponse]
    
class BookRequest(BaseModel):
    description: str | None = None
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
        
class BookLists(BaseModel):
    data: List[BookResponse]

 
      

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
    id: str
    access_token: str
    expires_at: datetime | None
    refresh_token: str
    refresh_token_expires_at: datetime | None

