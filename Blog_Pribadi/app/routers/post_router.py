from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.db import get_db
from app.database.models import Post, User
from app.schema.post_schema import PostCreate, PostUpdate, PostResponse
from app.core.security import get_current_user
from app.services import post_service

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/")
def create_post(
    data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ⬅️ DI SINI
):
    return post_service.create_post(db, data, current_user.id
    )


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post tidak ditemukan")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Tidak punya akses")

    db.delete(post)
    db.commit()
    return {"message": "Post berhasil dihapus"}

@router.get("/", response_model=List[PostResponse])
def list_posts(db: Session = Depends(get_db)):
    """
    Menampilkan daftar seluruh posting blog.
    """
    return post_service.get_posts(db)

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """
    Menampilkan detail satu posting berdasarkan ID.
    """
    post = post_service.get_post_detail(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post tidak ditemukan")
    return post

@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    data: PostUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Mengedit posting blog milik user yang sedang login.
    """
    post = post_service.edit_post(
        db,
        post_id,
        data.title,
        data.content,
        current_user.id
    )
    if not post:
        raise HTTPException(status_code=404, detail="Post tidak ditemukan")
    return post
