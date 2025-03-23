from pydantic import BaseModel

class BaseRequest(BaseModel):
    pass


class UserListRequest(BaseRequest):
    description: str
    price: int
    in_stock: bool
    
class AddBookRequest(BaseRequest):
    description: str
    price: int
    in_stock: bool