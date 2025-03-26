from pydantic import BaseModel,ConfigDict


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
    email: str
    password: str
    


class BaseResquest(UserRequest):
    r"""
        Pydantic v2 
    """
    id: int   
    model_config = ConfigDict(from_attributes=True)



class Token(BaseResquest):
    access_token: str
    token_type: str = "Bearer"
    expires_at: int
    refresh_token: str
    refresh_token_expires_at: int

    