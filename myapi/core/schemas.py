from pydantic import BaseModel

class BookRequest(BaseModel):
    description: str
    price: int

class BookResponse(BookRequest):
    id: int
    
    class Config:
        orm_mode = True    
