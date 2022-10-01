from typing import Optional

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.db.db_conf import Base


class Author(Base):
    __tablename__ = "authors"
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, nullable=False, unique=True)
    age: int = Column(Integer)
    books: list["Book"] = relationship(
        "Book", lazy="joined", back_populates="author"
    )

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class Book(Base):
    __tablename__ = "books"
    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(
        String, nullable=False
    )  # you can also define the amount or the limits
    author_id: Optional[int] = Column(
        Integer, ForeignKey(Author.id), nullable=True
    )
    author: Optional[Author] = relationship(
        Author, lazy="joined", back_populates="books"
    )
    rating: int = Column(Integer)

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
