from fastapi import FastAPI, HTTPException , Request
import logging
from app.models import Book

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from api.endpoints.book import book  

from database.database import  engine, Base , create_tables , async_session
from contextlib import asynccontextmanager




@asynccontextmanager
async def lifespan(app: FastAPI):
    
    print("🚀 서버 시작: 데이터베이스 초기화 중...")
    async with create_tables():
        yield
    print("🛑 서버 종료: 데이터베이스 연결 닫기")
    await engine.dispose()
    

    
app = FastAPI(lifespan=lifespan)



app.include_router(book)


origins: list[str] = [
    "localhost:8000",
    "localhost", 
    "127.0.0.1"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts = origins
)



####################################################################



@app.get("/")
async def root(req: Request):
    print(req.headers['host'])
    return {"message": "Hello FastAPI"}
