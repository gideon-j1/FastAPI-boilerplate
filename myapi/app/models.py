from sqlalchemy import Integer,String
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    
class AuthUser(Base):
    __tablename__ = 'AuthUser'
    
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True , autoincrement=True
    )
    
    r"""
     
     unqiue: 이메일 중복 방지 (데이터 무결성 보장)
     
    """
    email: Mapped[str] = mapped_column(
        String(30), nullable=False , unique=True
    )
    
    password: Mapped[str] = mapped_column(
        String(200) , nullable=False
    )