"""
Modul ini berisi business logic yang berkaitan dengan pengelolaan Post.
Digunakan untuk:
- Membuat objek Post
- Mengambil daftar dan detail posting
- Mengedit posting dengan validasi kepemilikan
- Menyimpan posting ke database

Modul ini dipanggil oleh router Post.
"""
from app.database.models import Post
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import post_repository
from datetime import datetime

# =========================================================
# BUILD POST OBJECT
# =========================================================
def build_post(data, user_id: int):
    """
    Membuat objek Post dari data input.

    Fungsi ini hanya membangun objek Post tanpa langsung
    menyimpannya ke database.

    Args:
        data: Data input posting (biasanya PostCreate schema).
        user_id (int): ID user yang menjadi penulis posting.

    Returns:
        Post: Objek Post yang siap disimpan ke database.
    """
    return Post(
        title=data.title,
        content=data.content,
        category_id=data.category_id,
        user_id=user_id
    )

# =========================================================
# GET POSTS
# =========================================================
def get_posts(db: Session):
    """
    Mengambil seluruh data posting blog.

    Args:
        db (Session): Session database SQLAlchemy.

    Returns:
        list[Post]: Daftar seluruh posting.
    """
    return post_repository.get_all_posts(db)


def get_post_detail(db: Session, post_id: int):
    """
    Mengambil detail satu posting berdasarkan ID.

    Args:
        db (Session): Session database SQLAlchemy.
        post_id (int): ID posting.

    Returns:
        Post | None: Objek Post jika ditemukan, None jika tidak.
    """
    return post_repository.get_post_by_id(db, post_id)


# =========================================================
# EDIT POST
# =========================================================
def edit_post(db: Session, post_id: int, title: str, content: str, user_id: int):
    """
    Mengedit posting blog milik user yang sedang login.

    Fungsi ini akan:
    - Mengecek apakah posting ada
    - Memastikan user adalah pemilik posting
    - Memperbarui judul dan konten posting

    Args:
        db (Session): Session database SQLAlchemy.
        post_id (int): ID posting yang akan diedit.
        title (str): Judul baru posting.
        content (str): Konten baru posting.
        user_id (int): ID user yang sedang login.

    Returns:
        Post | None: Objek Post yang telah diperbarui,
        atau None jika posting tidak ditemukan.

    Raises:
        HTTPException: Jika user bukan pemilik posting.
    """
    post = post_repository.get_post_by_id(db, post_id)
    if not post:
        return None

    if post.user_id != user_id:
        raise HTTPException(status_code=403, detail="Tidak diizinkan")

    post.title = title
    post.content = content
    db.commit()
    db.refresh(post)
    return post

# =========================================================
# CREATE POST
# =========================================================
def create_post(db: Session, data, user_id: int):
    """
    Menyimpan posting blog baru ke database.

    Args:
        db (Session): Session database SQLAlchemy.
        data: Data input posting (biasanya PostCreate schema).
        user_id (int): ID user yang menjadi penulis posting.

    Returns:
        Post: Objek Post yang berhasil disimpan.
    """
    post = Post(
        title=data.title,
        content=data.content,
        user_id=user_id,
        category_id=data.category_id,
        created_at=datetime.utcnow()
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post