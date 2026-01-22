from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CommentCreate(BaseModel):
    """Schema untuk membuat komentar baru.
    
    Attributes:
        content (str): Isi/teks komentar
    """
    content: str


class CommentResponse(BaseModel):
    """Schema untuk respons data komentar.
    
    Attributes:
        id (int): ID unik komentar
        content (str): Isi komentar
        user_id (int): ID user komentator
        username (str): Nama user komentator
        post_id (int): ID postingan yang dikomentar
        created_at (datetime): Waktu pembuatan komentar
    
    Config:
        from_attributes: Mengizinkan konversi dari ORM objects
    """
    id: int
    content: str
    user_id: int
    username: str
    post_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
