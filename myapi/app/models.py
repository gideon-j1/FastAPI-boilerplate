from pydantic import BaseModel
from sqlalchemy import Column,Integer,String,TIMESTAMP,Boolean,text
import uuid
from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, String, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    update_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Item(Base):
    __tablename__ = 'book items'
    
    user_id: Mapped[int] = mapped_column(
        Uuid(as_uuid=False), primary_key=True ,default=lambda _: str(uuid.uuid4())
    )
    
    description: Mapped[str] = mapped_column(
        String(256), nullable=False
    )
    
    price: Mapped[int] = mapped_column(
        BigInteger , nullable=False
    )