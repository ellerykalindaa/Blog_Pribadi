from pydantic import BaseModel
from datetime import datetime

class PostCreate(BaseModel):
    title: str
    content: str
    category_id: int

class PostUpdate(BaseModel):
    title: str
    content: str
    category_id: int

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    author_id: int

    class Config:
        from_attributes = True