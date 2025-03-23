from fastapi import APIRouter
from app.models import Item
from fastapi import Depends
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse

from core.schemas import UserListRequest

from database.database import get_session
from fastapi.middleware.trustedhost import TrustedHostMiddleware

book = APIRouter()


# @app.get("/favicon.ico", response_class=HTMLResponse)
# async def favicon():
#     return Response(content="", media_type="image/x-icon")




@book.get("/h")
async def hello():
    return {"message": "안녕하세요 파이보"}




# @router.get("/lists",response_model=UserListRequest, description="Get book list")
# async def get_books(
#     lists: Item = Depends(get_session)    
# ) -> None:
    
#     print(lists)
#     return lists

# @router.post("/add/book",response_model=,description='Post book 1')
# async def add_book(
#     item: Item =Depends(get_session)
# ) -> None:
#     return item

