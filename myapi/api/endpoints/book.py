from app.models import Book
from database.database import get_db

from core.schemas import (
    BookRequest,
    BookResponse,
)


from fastapi import (
    status,
    APIRouter,
    Depends,   
    HTTPException
)

try:
    from sqlalchemy import insert,select , delete
    from sqlalchemy.ext.asyncio import AsyncSession
    
except ImportError:
    raise ImportError("Please install sqlachemy")



book = APIRouter()

@book.post("/add", description="Add book", status_code=status.HTTP_201_CREATED)

async def add_book(payload: BookRequest, db: AsyncSession = Depends(get_db)) -> None:
    
    if payload.description == "" or payload.price == "":
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
    new_book = Book(description=payload.description,price=payload.price)
   
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    
    return {"message" : "성공입니다"}
    

@book.get("/lists", description="Get book list", status_code=status.HTTP_200_OK)
async def get_books(
    db: AsyncSession = Depends(get_db)    
) -> dict:

    stmt = select(Book)
    
    books = await db.execute(stmt)
    lists = books.scalars().all()  
      
    for b in lists:
        print(vars(b))
    
    return {"message" : "성공입니다", "list" : [BookResponse.model_validate(b) for b in lists]}


@book.delete("/delete/{user_id}",description="delete book", status_code=status.HTTP_200_OK)
async def delete_book(
    user_id: int,
    db: AsyncSession = Depends(get_db)
) -> None:
    

    stmt = select(Book).where(Book.id == user_id)
    book = await db.execute(stmt)
        
    db_book = book.scalar_one_or_none()
    
    if not db_book:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    await db.delete(db_book)
    await db.commit()
 
    return {"message" : "성공입니다."}


@book.put("/update/{user_id}",description="update price",status_code=status.HTTP_201_CREATED)
async def update_price(
    user_id: int,
    payload : BookRequest,
    db: AsyncSession = Depends(get_db)
) -> None:
    
    stmt = select(Book).where(Book.id == user_id)
    book = await db.execute(stmt)
    
    db_book = book.scalar_one_or_none()
    
    if not db_book:
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    db_book.price = payload.price
    
    await db.commit()
    await db.refresh(db_book)
    
    return {"message" : "성공입니다."}


@book.get("/lists_price",description="Get book list price", status_code=status.HTTP_200_OK)
async def get_book_price(
    db:AsyncSession = Depends(get_db)
) -> None:
    
    stmt = select(Book).where(Book.price < 100)
    prices = await db.execute(stmt)
    lists = prices.scalars().all() 
    
    if not lists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    
    for b in lists:
        print(vars(b))
    
    return {
        "message": "성공입니다.",
        "lists": [BookResponse.model_validate(b) for b in lists]
    }