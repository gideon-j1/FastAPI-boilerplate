from app.models import Book
from core.schemas import BookRequest,BookResponse
from database.database import get_db
from fastapi import APIRouter , Depends , HTTPException , Response , Request


try:
    
    from sqlalchemy import insert,select , delete
    from sqlalchemy.ext.asyncio import AsyncSession
    
except ImportError:
    raise ImportError("Please install sqlachemy")

from core.handler import UnicornException

book = APIRouter()

@book.post("/add", description="Add book")
async def add_book(payload: BookRequest, db: AsyncSession = Depends(get_db)) -> None:
    
    if payload.description == "" or payload.price == "":
        UnicornException(statuss_code=500)
        
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
        UnicornException(status_code=500)
    
    await db.delete(db_book)
    await db.commit()
 
    return {"message" : "성공입니다."}


@book.put("/update/{user_id}",description="update price")
async def update_price(
    user_id: int,
    payload : BookRequest,
    db: AsyncSession = Depends(get_db)
) -> None:
    
    stmt = select(Book).where(Book.id == user_id)
    book = await db.execute(stmt)
    
    db_book = book.scalar_one_or_none()
    
    if not db_book:
         UnicornException(status_code=500)
    
    db_book.price = payload.price
    
    await db.commit()
    await db.refresh(db_book)
    
    return {"message" : "성공입니다."}
