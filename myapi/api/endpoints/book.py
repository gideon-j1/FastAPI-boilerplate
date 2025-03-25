from app.models import Book
from core.schemas import BookRequest,BookResponse
from database.database import create_tables , get_db
from fastapi import APIRouter , Depends , HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
    
from sqlalchemy import insert,select , delete


book = APIRouter()

@book.post("/add", description="Add book")
async def add_book(payload: BookRequest, db: AsyncSession = Depends(get_db)) -> None:
    
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
    
    return {"message" : "성공입니다", "list" : [BookResponse.model_validate(b) for b in lists]}



@book.delete("/delete/{user_id}",description="delete book")
async def delete_book(
    user_id: int,
    db: AsyncSession = Depends(get_db)
) -> None:
    
    stmt = select(Book).where(Book.id == user_id)
    book = await db.execute(stmt)
        
    db_book = book.scalar_one_or_none()

    if not db_book:
        raise HTTPException(status_code=404,detail="Book not fount")
    
    await db.delete(db_book)
    await db.commit()
 
    
    
    return {"message" : "성공입니다."}

