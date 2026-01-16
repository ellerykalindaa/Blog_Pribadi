from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class PostCreate(BaseModel):
    title: str
    content: str
    category_id: Optional[int] = None

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
    category_id: Optional[int]

    class Config:
        from_attributes = True 

class CommentResponse(BaseModel):
    id: int
    content: str
    user_id: int
    post_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

