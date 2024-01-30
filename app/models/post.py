from sqlalchemy import Column, Integer, DateTime, String
from app.config.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    rating = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
