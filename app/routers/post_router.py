from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.orm import joinedload

from app.database.db import get_db
from app.database.models import User, Post
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
    """Membuat postingan blog baru.
    
    Args:
        data (PostCreate): Judul, konten, dan kategori postingan
        db (Session): Database session
        current_user (User): User yang sedang login
        
    Returns:
        PostResponse: Data postingan yang baru dibuat beserta username penulis
    """
    # PAKAI SERVICE
    post = post_service.create_post(db, data, current_user.id)
    
    # AMBIL POST DENGAN USER DATA MENGGUNAKAN JOINLOAD
    post_with_author = db.query(Post).options(
        joinedload(Post.author)
    ).filter(Post.id == post.id).first()
    
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        created_at=post.created_at,
        author_id=post.author_id,
        username=post_with_author.author.username,
        category_id=post.category_id
    )

@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Menghapus postingan milik user yang sedang login.
    
    Args:
        post_id (int): ID postingan yang akan dihapus
        db (Session): Database session
        current_user: User yang sedang login
        
    Returns:
        dict: Message sukses/error
        
    Raises:
        HTTPException: 404 jika postingan tidak ditemukan, 403 jika bukan pemilik
    """
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
    """Menampilkan daftar seluruh posting blog.
    
    Args:
        db (Session): Database session
        
    Returns:
        List[PostResponse]: Daftar semua postingan dengan info penulis
    """
    # PAKAI SERVICE YANG SUDAH DIPERBAIKI
    return post_service.get_posts(db)

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Menampilkan detail satu posting berdasarkan ID.
    
    Args:
        post_id (int): ID postingan
        db (Session): Database session
        
    Returns:
        PostResponse: Data postingan dengan info penulis
        
    Raises:
        HTTPException: 404 jika postingan tidak ditemukan
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
    """Mengedit posting blog milik user yang sedang login.
    
    Args:
        post_id (int): ID postingan yang akan diedit
        data (PostUpdate): Data postingan baru
        db (Session): Database session
        current_user: User yang sedang login
        
    Returns:
        PostResponse: Data postingan yang sudah diperbarui
        
    Raises:
        HTTPException: 403 jika bukan pemilik, 404 jika tidak ditemukan
    """
    post = db.query(Post).get(post_id)
    if not post:
        raise HTTPException(404)

    if post.author_id != current_user.id:
        raise HTTPException(403)

    post.title = data.title
    post.content = data.content
    if hasattr(data, 'category_id'):
        post.category_id = data.category_id
    
    db.commit()
    db.refresh(post)
    
    # AMBIL LAGI DENGAN USER DATA
    post_with_author = db.query(Post).options(
        joinedload(Post.author)
    ).filter(Post.id == post.id).first()
    
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        created_at=post.created_at,
        author_id=post.author_id,
        username=post_with_author.author.username,
        category_id=post.category_id
    )