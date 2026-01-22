from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class PostCreate(BaseModel):
    """Schema untuk membuat postingan baru.
    
    Attributes:
        title (str): Judul postingan, max 200 karakter
        content (str): Isi/konten postingan
        category_id (Optional[int]): ID kategori postingan
    """
    title: str
    content: str
    category_id: Optional[int] = None

class PostUpdate(BaseModel):
    """Schema untuk mengupdate postingan.
    
    Attributes:
        title (str): Judul postingan diperbarui
        content (str): Konten postingan diperbarui
        category_id (Optional[int]): ID kategori postingan
    """
    title: str
    content: str
    category_id: Optional[int] = None

class CategoryResponse(BaseModel):
    """Schema untuk respons data kategori.
    
    Attributes:
        id (int): ID unik kategori
        name (str): Nama kategori
    
    Config:
        from_attributes: Mengizinkan konversi dari ORM objects
    """
    id: int
    name: str
    
    model_config = ConfigDict(from_attributes=True)

class PostResponse(BaseModel):
    """Schema untuk respons data postingan.
    
    Attributes:
        id (int): ID unik postingan
        title (str): Judul postingan
        content (str): Isi postingan
        created_at (datetime): Waktu pembuatan
        author_id (int): ID user penulis
        username (str): Nama user penulis
        category_id (Optional[int]): ID kategori
        category (Optional[CategoryResponse]): Objek kategori dengan nama
    
    Config:
        from_attributes: Mengizinkan konversi dari ORM objects
    """
    id: int
    title: str
    content: str
    created_at: datetime
    author_id: int
    username: str
    category_id: Optional[int] = None
    category: Optional[CategoryResponse] = None

    model_config = ConfigDict(from_attributes=True)

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