from sqlalchemy.engine.url import URL
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.config import get_settings


def new_async_engine(uri : URL) -> AsyncEngine:
    return create_async_engine(
        uri,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30.0,
        pool_recycle=600,
    )

engine = new_async_engine(get_settings().sqlalchemy_database_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)


r"""
    데이터베이스 세션 생성
"""
def get_async_db():
    db = async_session()    
    try:
        yield db
    finally:
        db.close()
        

r"""
    데이터베이스 관리하는 함수 get_async_db() 생명 주기 관리 
    컨텍스트 내에서 적절하게 자동으로 닫히고 열리게끔 
"""
async def get_session() -> AsyncGenerator[AsyncSession]:
    async with get_async_db as session:
        yield session