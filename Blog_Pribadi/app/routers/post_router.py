from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.db import get_db
from app.database.models import Post, User
from app.schema.post_schema import PostCreate, PostUpdate, PostResponse
from app.core.security import get_current_user
from app.services import post_service

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostResponse)
def create_post(
    data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    post = Post(
        title=data.title,
        content=data.content,
        author_id=current_user.id,
        author_id=current_user.id
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post tidak ditemukan")

    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Tidak punya akses")

    db.delete(post)
    db.commit()
    return {"message": "Post berhasil dihapus"}

@router.get("/", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    """
    Menampilkan daftar seluruh posting blog.
    """
    return db.query(Post).all()

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """
    Menampilkan detail satu posting berdasarkan ID.
    """
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(404)
    return post

@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    data: PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Mengedit posting blog milik user yang sedang login.
    """
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(404)

    if post.author_id != current_user.id:
        raise HTTPException(403)

    post.title = data.title
    post.content = data.content
    db.commit()
    db.refresh(post)
    return post

