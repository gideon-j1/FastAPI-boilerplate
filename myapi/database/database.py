from sqlalchemy.engine.url import URL
from collections.abc import AsyncGenerator



from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from contextlib import asynccontextmanager

from app.models import Base

from content import SQLALCHEMY_DATABASE_URL


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
#Factory session이 필요한 이유 트랜잭션 (crud를 수행하기 위해 필요 )
async_session =async_sessionmaker(autocommit=False,bind=engine,expire_on_commit=False)


@asynccontextmanager
async def create_tables():
    if engine is None:
        raise Exception("DatabaseSessionManger is not initialzed")
    async with engine.begin() as conn:

        try:           
            await conn.run_sync(Base.metadata.create_all)
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




