from app.models import Book
from core.schemas import BookRequest
from database.database import create_tables , get_db
from fastapi import APIRouter , Depends
from sqlalchemy.ext.asyncio import AsyncSession
    
from sqlalchemy import insert,select


book = APIRouter()

@book.post("/add", description="Add book")
async def hello(payload: BookRequest, db: AsyncSession = Depends(get_db)) -> None:
    print(payload.price)
    
    new_book = Book(description=payload.description,price=payload.price)
    
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    
    return {"message" : "성공입니다"}
    

@book.get("/lists", description="Get book list")
async def get_books(
    db: AsyncSession = Depends(get_db)    
) -> dict:

    stmt = select(Book)
    
    books = await db.execute(stmt)
    lists = books.scalars().all()  
      
    for b in lists:
        print(vars(b))
    
    return {"message" : "성공입니다"}



