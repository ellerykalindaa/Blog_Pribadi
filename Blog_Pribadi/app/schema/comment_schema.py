"""
Modul ini berisi definisi schema Pydantic untuk entitas Comment.
Digunakan untuk:
- Validasi data komentar dari client
- Menentukan format response komentar ke client

Schema ini digunakan pada endpoint komentar (comments).
"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CommentCreate(BaseModel):
    """
    Schema untuk membuat komentar baru.

    Digunakan sebagai request body pada endpoint:
    POST /comments/posts/{post_id}
    """
    content: str


class CommentResponse(BaseModel):
    """
    Schema response komentar.

    Digunakan untuk mengembalikan data komentar ke client,
    termasuk informasi user, post, dan waktu pembuatan.
    """
    id: int
    content: str
    user_id: int
    post_id: int
    created_at: datetime

    # Mengizinkan Pydantic membaca data dari ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)
