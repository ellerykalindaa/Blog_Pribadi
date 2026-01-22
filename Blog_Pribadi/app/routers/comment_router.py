"""
Router ini menangani endpoint yang berkaitan dengan komentar
pada artikel blog.

Fitur:
- Menambahkan komentar pada post
- Mengambil daftar komentar berdasarkan post

Endpoint berada di bawah prefix '/comments'.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.db import get_db
from app.database.models import Comment, Post
from app.schema.comment_schema import CommentCreate
from app.core.security import get_current_user
from app.schema.comment_schema import CommentResponse

# =========================================================
# ROUTER CONFIGURATION
# =========================================================
router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

# =========================================================
# ADD COMMENT TO POST
# =========================================================
@router.post("/posts/{post_id}")
def add_comment(
    post_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    """
    Endpoint untuk menambahkan komentar pada sebuah post.

    Endpoint ini hanya dapat diakses oleh user yang sudah login.

    Args:
        post_id (int): ID post yang akan dikomentari.
        data (CommentCreate): Data komentar.
        db (Session): Session database SQLAlchemy.
        current_user (User): User yang sedang login.

    Returns:
        Comment: Data komentar yang berhasil ditambahkan.

    Raises:
        HTTPException: Jika post tidak ditemukan.
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=404, 
            detail="Post tidak ditemukan"
        )

    comment = Comment(
        content=data.content,
        user_id=current_user.id,
        post_id=post_id
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment

# =========================================================
# GET COMMENTS BY POST
# =========================================================
@router.get("/posts/{post_id}", response_model=List[CommentResponse])
def get_comments_by_post(
    post_id: int,
    db: Session = Depends(get_db)
):

    """
    Endpoint untuk mengambil daftar komentar berdasarkan post.

    Args:
        post_id (int): ID post.
        db (Session): Session database SQLAlchemy.

    Returns:
        List[CommentResponse]: Daftar komentar pada post.

    Raises:
        HTTPException: Jika post tidak ditemukan.
    """
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=404, 
            detail="Post tidak ditemukan"
        )

    return db.query(Comment).filter(Comment.post_id == post_id).all()