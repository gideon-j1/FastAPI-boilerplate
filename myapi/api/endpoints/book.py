from app.models import Book
from core.schemas import BookRequest , BookResponse
from database.database import create_tables , get_db
from fastapi import APIRouter , Depends
from sqlalchemy.ext.asyncio import AsyncSession
    
from sqlalchemy import insert

book = APIRouter()

@book.post("/add", response_model=BookResponse , description="Add book")
async def hello(payload: BookRequest, db: AsyncSession = Depends(get_db)) -> None:
    print(payload.price)
    
    new_book = Book(description=payload.description,price=payload.price)
    
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    
    return {"message": "안녕하세요"}

@book.get("/lists", description="Get book list")
async def get_books(
    db: AsyncSession = Depends(get_db)    
) -> None:
    
    result = await db.execute("SELECT * FROM book")
    users = result.mappings().all()
    
    print(users)
    return users




