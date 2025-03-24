from app.models import Book
from core.schemas import BookRequest
from database.database import create_tables , get_db
from fastapi import APIRouter , Depends
from sqlalchemy.ext.asyncio import AsyncSession
    
    

from typing import Any


book = APIRouter()

@book.get("/h")
async def hello(db: AsyncSession = Depends(get_db)) -> None:
    
    book = Book(description='test' , price=5000)
    db.add(book)
    db.commit()
    
    # result = await db.execute("SELECT * FROM book")
    # print(result)
    return {"message": "안녕하세요"}

@book.get("/lists", description="Get book list")
async def get_books(
    db: AsyncSession = Depends(get_db)    
) -> None:
    
    result = await db.execute("SELECT * FROM book")
    users = result.mappings().all()
    
    print(users)
    return users


# @book.post("/add",response_model=BookRequest, description="Add book")
# async def add_book(
#     item: Book,
#     session: AsyncSession = Depends(get_session)
# ) -> Any: 
    
#     new_book = Book(description=item.description , price = item.price)
#     session.add(new_book)
    
#     await session.commit()
#     await session.refresh(new_book)
    
#     return {"message" : "Book created" , "item" : new_book}
    
#     return 

# @router.post("/add/book",response_model=,description='Post book 1')
# async def add_book(
#     item: Item =Depends(get_session)
# ) -> None:
#     return item

