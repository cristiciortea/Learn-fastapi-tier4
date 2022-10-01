from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from src.db.db_conf import Base


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)  # you can also define the amount or the limits
    author = Column(String)
    content = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
