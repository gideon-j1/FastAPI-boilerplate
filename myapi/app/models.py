from pydantic import BaseModel
from sqlalchemy import Column,Integer,String,TIMESTAMP,Boolean,text
import uuid
from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

from sqlalchemy.orm import declarative_base
Base = declarative_base()


class Book(Base):
    __tablename__ = 'book'
    
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    description: Mapped[str] = mapped_column(
        String(256), nullable=False
    )
    
    price: Mapped[int] = mapped_column(
        Integer , nullable=False
    )
    
    