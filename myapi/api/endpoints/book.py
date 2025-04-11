from app.models import Book
from database.database import get_db ,metadata  ,engine,async_new_book

from core.schemas import (
    BookRequest,
    BookResponse,
    NewBookResponse,
    PartitionResponse,
    BookLists,
)

from typing import (
    Any
)

from fastapi import (
    status,
    APIRouter,
    Depends,   
    HTTPException,
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
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="descript or price empty"
            )
        
    new_book = Book(description=payload.description,price=payload.price)
   
    db.add(new_book)
    await db.commit()
    await db.refresh(new_book)
    
    return {"message" : "성공입니다"}
    

@book.get("/lists", 
          description="Get book list",
          response_model=BookLists,
          status_code=status.HTTP_200_OK)
async def get_books(
    db: AsyncSession = Depends(get_db),
) -> dict:

    stmt = select(Book)
    
    books = await db.execute(stmt)
    lists = books.scalars().all()  
    
    if not lists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="list not found Plesas add book"
            )
      
    for b in lists:
        print(vars(b))
    
    return {"data" : [BookResponse.model_validate(b) for b in lists]}


@book.delete("/delete/{user_id}",description="delete book", status_code=status.HTTP_200_OK)
async def delete_book(
    user_id: int,
    db: AsyncSession = Depends(get_db)
) -> None:
    
    stmt = select(Book).where(Book.id == user_id)
    book = await db.execute(stmt)
        
    db_book = book.scalar_one_or_none()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="book id not found"
            )
    
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
    
    if db_book.price == payload.price:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="duplicate input price"
        )
    
    if not db_book:
         raise HTTPException(
             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
             detail="price empty"
             )
         
    
    db_book.price = payload.price
    
    await db.commit()
    await db.refresh(db_book)
    
    return {"message" : "성공입니다."}


@book.get("/lists_price",
          description="Get book list price",
          response_model=BookLists, 
          status_code=status.HTTP_200_OK)
async def get_book_price(
    db:AsyncSession = Depends(get_db)
) -> dict:
    
    stmt = select(Book).where(Book.price < 100)
    prices = await db.execute(stmt)
    lists = prices.scalars().all() 
    
    if not lists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="book price empyt"                
            )
    
    for b in lists:
        print(vars(b))
    
    return {"data": [BookResponse.model_validate(b) for b in lists]}
    
########################## LIST Partiotion ##########################

r"""
                            ------ PSQL command line ------
    1. CREATE TABLE new_book (
        id INTEGER,
        description TEXT,
        price INTEGER,
        PRIMARY KEY (id, price)  -- 가격(price)도 기본키의 일부로 추가
    PARTITION BY LIST (price);
    파티셔닝 상위 테이블 생성
    
    
    2. create table new_book_fisrt PARTITION OF new_book FOR VALUES IN (0,1,2,3,4,5);
    create table new_book_second PARTITION OF new_book FOR VALUES IN (6,7,8,9,10,11);
    파티셔닝 하위 테이블 생성

    3. \d+ new_book;
    조회 
        
    4. Insert into new_book (id,description,price) select id , description , price from book;
    기존테이블 => 파티셔닝 테이블 마이그레이션
    
    5. SELECT tableoid::regclass,* FROM new_book;
    마이그레이션 된 new_book 조회 (get_new_book)
    
"""

@book.get("/partitions",description="get partition list",
          response_model=PartitionResponse,
          status_code=status.HTTP_200_OK)
async def get_new_book(
    db:AsyncSession = Depends(get_db)
) -> dict:
    
    new_book = await async_new_book()  
    
    if not new_book:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "not prepare partions query"
            )

    
    first_dict = []
    second_dict = []
    
    for tup in new_book:
        key = tup[0]
        values = tup[1:]
                
        if key == "new_book_fisrt":
            

            first_dict.extend([
                {
                "tableoid" : key,
                "id" : values[0],
                "description" : values[1],
                "price" : values[2]    
                }
            ])
            
            
        elif key == "new_book_second":
            second_dict.extend([
                {
                "tableoid" : key,
                "id" : values[0],
                "description" : values[1],
                "price" : values[2]    
                }
            ])
        
    for val in first_dict + second_dict:
        if not isinstance(val,dict):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="not type dict")
        
    
    return {
        "first" : first_dict,
        "second" : second_dict
    }
