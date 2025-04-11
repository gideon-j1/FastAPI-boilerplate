from sqlalchemy.engine.url import URL
from collections.abc import AsyncGenerator

from sqlalchemy import MetaData, Table

from sqlalchemy import text

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from contextlib import asynccontextmanager

from app.models import Base

from content import SQLALCHEMY_DATABASE_URL

try:
    import redis
except ImportError:
    raise ImportError("Pleas install redis")

def new_async_engine(uri : URL) -> AsyncEngine:
    return create_async_engine(
        uri,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30.0,
        pool_recycle=600,
    )

# 인스턴스
engine = new_async_engine(SQLALCHEMY_DATABASE_URL)
#Factory session이 필요한 이유 트랜잭션 (orm 방식으로 crud를 수행하기 위해 필요 )
async_session =async_sessionmaker(autocommit=False,bind=engine,expire_on_commit=False)

# 메타데이터 객체 생성
metadata = MetaData()



# 기존에 데이터베이스 있는 table 참조 (new_book)
async def async_new_book():
        async with engine.connect() as conn:
                            
            r"""
                ORM 방식으로 쿼리 추출 근데 이렇게 하면 복잡한 쿼리는 힘들수 있으니 직접쿼리 날리고 싶을때는 engine에 접근해서 쿼리 작성하자.
                    
                    await conn.run_sync(metadata.reflect, only=["new_book"])
                    
                    new_book = Table("new_book", metadata, autoload_with=engine)
                    
                    print("tables: ", new_book, type(new_book))
                    
                    return new_book
            """
            new_book = await conn.execute(text("SELECT tableoid::regclass, * FROM new_book;"))
            rows = new_book.all()
            
            
            return rows


@asynccontextmanager
async def create_tables():
    if engine is None:
        raise Exception("DatabaseSessionManger is not initialzed")
    async with engine.begin() as conn:

        try:           
            await conn.run_sync(Base.metadata.create_all)
            # await async_new_book()
        except Exception:
            await conn.rollback()
            raise
    yield
    


async def get_db() -> AsyncGenerator[AsyncSession]:
    db = async_session()
    try:
        yield db
    finally:
        await db.close()

############################# Redis DB ###############################
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0
)

