"""
Router ini menangani endpoint yang berkaitan dengan posting blog,
meliputi:
- Membuat post baru
- Mengambil daftar post
- Mengambil detail post
- Mengedit post
- Menghapus post

Endpoint berada di bawah prefix '/posts'.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.db import get_db
from app.database.models import Post
from app.schema.post_schema import PostCreate, PostUpdate, PostResponse
from app.core.security import get_current_user

router = APIRouter(
    prefix="/posts", 
    tags=["Posts"]
)

# =========================================================
# CREATE POST
# =========================================================
@router.post("/", response_model=PostResponse)
def create_post(
    data: PostCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Endpoint untuk membuat posting blog baru.

    Hanya user yang sudah login yang dapat membuat post.

    Args:
        data (PostCreate): Data post baru.
        db (Session): Session database SQLAlchemy.
        current_user (User): User yang sedang login.

    Returns:
        PostResponse: Data post yang berhasil dibuat.
    """
    post = Post(
        title=data.title,
        content=data.content,
        author_id=current_user.id,
        category_id=data.category_id 
    )

    db.add(post)
    db.commit()
    db.refresh(post)
    return post

# =========================================================
# DELETE POST
# =========================================================
@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Endpoint untuk menghapus posting blog.

    Hanya pemilik post yang dapat menghapus post.

    Args:
        post_id (int): ID post.
        db (Session): Session database SQLAlchemy.
        current_user (User): User yang sedang login.

    Returns:
        dict: Pesan keberhasilan penghapusan post.

    Raises:
        HTTPException: Jika post tidak ditemukan atau tidak memiliki akses.
    """
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(
            status_code=404, 
            detail="Post tidak ditemukan"
        )

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="Tidak punya akses"
        )

    db.delete(post)
    db.commit()
    return {"message": "Post berhasil dihapus"}

# =========================================================
# GET ALL POSTS
# =========================================================
@router.get("/", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    """
    Endpoint untuk mengambil seluruh posting blog.

    Args:
        db (Session): Session database SQLAlchemy.

    Returns:
        List[PostResponse]: Daftar seluruh post.
    """
    return db.query(Post).all()

# =========================================================
# GET POST BY ID
# =========================================================
@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """
    Endpoint untuk mengambil detail post berdasarkan ID.

    Args:
        post_id (int): ID post.
        db (Session): Session database SQLAlchemy.

    Returns:
        PostResponse: Detail post.

    Raises:
        HTTPException: Jika post tidak ditemukan.
    """
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post tidak ditemukan"
        )
    
    return post

# =========================================================
# UPDATE POST
# =========================================================
@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    data: PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Endpoint untuk mengedit posting blog.

    Hanya pemilik post yang dapat mengedit post.

    Args:
        post_id (int): ID post.
        data (PostUpdate): Data post yang diperbarui.
        db (Session): Session database SQLAlchemy.
        current_user (User): User yang sedang login.

    Returns:
        PostResponse: Data post setelah diperbarui.
    """
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post idak ditemukan"
        )

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Tidak punya akses"
        )

    post.title = data.title
    post.content = data.content
    db.commit()
    db.refresh(post)
    return post