from fastapi import FastAPI, HTTPException , Request
import logging
from app.models import Item

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from core.config import get_settings



app = FastAPI()

from api.endpoints.book import book  
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

@app.get("/")
async def root(req: Request):
    print(req.headers['host'])
    return {"message": "Hello FastAPI"}


