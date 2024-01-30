from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    rating: Optional[int] = None
    date_created: Optional[datetime] = None
    date_updated: Optional[datetime] = None

    # model_config = ConfigDict(from_attributes=True)
    class Config:
        orm_mode = True
