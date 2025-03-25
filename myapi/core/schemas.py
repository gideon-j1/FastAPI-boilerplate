from pydantic import BaseModel



class BookRequest(BaseModel):
    description: str
    price: int


