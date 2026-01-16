from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    content: str
    user_id: int
    post_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
