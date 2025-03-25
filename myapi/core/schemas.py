from pydantic import BaseModel



class BookRequest(BaseModel):
    description: str
    price: int

class BookResponse(BookRequest):
    id: str

    class Config:
        from_attributes = True
