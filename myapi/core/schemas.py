from pydantic import BaseModel, Field , ConfigDict ,  StringConstraints
from typing import Optional , Annotated


class BookRequest(BaseModel):
    description: str
    price: int

class BookResponse(BookRequest):
    id: int

    class Config:
        from_attributes = True
        
