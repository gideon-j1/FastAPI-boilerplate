from pydantic import BaseModel

class BaseRequest(BaseModel):
    pass


class BookRequest(BaseRequest):
    id: str
    description: str
    price: int
    
