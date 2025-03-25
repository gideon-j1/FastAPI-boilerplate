from sqlalchemy import Integer,String
from sqlalchemy import String
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
    
    