"""
Modul ini berisi definisi schema Pydantic untuk entitas Post dan Comment
yang berkaitan dengan Post.

Digunakan untuk:
- Validasi data posting blog dari client
- Menentukan format response posting ke client
- Menyediakan representasi data komentar pada posting
"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from app.schema.user_schema import AuthorResponse

class PostCreate(BaseModel):
    """
    Schema untuk membuat posting blog baru.

    Digunakan sebagai request body pada endpoint:
    POST /posts
    """
    title: str
    content: str
    category_id: int

class PostUpdate(BaseModel):
    """
    Schema untuk memperbarui posting blog.

    Digunakan sebagai request body pada endpoint:
    PUT /posts/{post_id}
    """
    title: str
    content: str
    category_id: int

class PostResponse(BaseModel):
    """
    Schema response posting blog.

    Digunakan untuk mengembalikan data posting ke client,
    termasuk informasi penulis, kategori, dan waktu pembuatan.
    """
    id: int
    title: str
    content: str
    created_at: datetime
    author_id: int              
    category_id: Optional[int]

    author: AuthorResponse

    # Mengizinkan Pydantic membaca data dari ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)

class CommentResponse(BaseModel):
    """
    Schema response komentar pada posting.

    Digunakan untuk menampilkan komentar yang terkait
    dengan suatu posting blog.
    """
    id: int
    content: str
    user_id: int
    post_id: int
    created_at: datetime

    # Mengizinkan Pydantic membaca data dari ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)