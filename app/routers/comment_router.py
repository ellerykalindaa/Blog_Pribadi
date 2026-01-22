from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import Comment, Post, User
from app.schema.comment_schema import CommentCreate, CommentResponse
from app.core.security import get_current_user
from typing import List

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@router.post("/posts/{post_id}", response_model=CommentResponse)
def add_comment(
    post_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Menambahkan komentar ke sebuah postingan blog.
    
    Hanya user yang sudah login yang dapat menambahkan komentar.
    
    Args:
        post_id (int): ID postingan yang akan dikomentar
        data (CommentCreate): Konten komentar
        db (Session): Database session
        current_user: User yang sedang login
        
    Returns:
        CommentResponse: Data komentar yang baru dibuat
        
    Raises:
        HTTPException: 404 jika postingan tidak ditemukan
    """

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post tidak ditemukan")

    comment = Comment(
        content=data.content,
        user_id=current_user.id,
        post_id=post_id
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    return CommentResponse(
        id=comment.id,
        content=comment.content,
        user_id=comment.user_id,
        username=current_user.username,
        post_id=comment.post_id,
        created_at=comment.created_at
    )

@router.get("/posts/{post_id}", response_model=List[CommentResponse])
def get_comments_by_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    """Menampilkan seluruh komentar pada satu postingan blog.
    
    Args:
        post_id (int): ID postingan
        db (Session): Database session
        
    Returns:
        List[CommentResponse]: Daftar semua komentar dengan info komentator
        
    Raises:
        HTTPException: 404 jika postingan tidak ditemukan
    """

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post tidak ditemukan")

    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    
    result = []
    for comment in comments:
        user = db.query(User).filter(User.id == comment.user_id).first()
        result.append(CommentResponse(
            id=comment.id,
            content=comment.content,
            user_id=comment.user_id,
            username=user.username if user else "Unknown",
            post_id=comment.post_id,
            created_at=comment.created_at
        ))
    
    return result


@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mengedit komentar milik user yang sedang login.
    
    Args:
        comment_id (int): ID komentar yang akan diedit
        data (CommentCreate): Konten komentar yang baru
        db (Session): Database session
        current_user: User yang sedang login
        
    Returns:
        CommentResponse: Data komentar yang sudah diperbarui
        
    Raises:
        HTTPException: 404 jika komentar tidak ditemukan, 403 jika bukan pemilik
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Komentar tidak ditemukan")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Anda tidak memiliki akses untuk mengedit komentar ini")

    comment.content = data.content
    db.commit()
    db.refresh(comment)

    return CommentResponse(
        id=comment.id,
        content=comment.content,
        user_id=comment.user_id,
        username=current_user.username,
        post_id=comment.post_id,
        created_at=comment.created_at
    )


@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Menghapus komentar milik user yang sedang login.
    
    Args:
        comment_id (int): ID komentar yang akan dihapus
        db (Session): Database session
        current_user: User yang sedang login
        
    Returns:
        dict: Message sukses penghapusan
        
    Raises:
        HTTPException: 404 jika komentar tidak ditemukan, 403 jika bukan pemilik
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Komentar tidak ditemukan")

    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Anda tidak memiliki akses untuk menghapus komentar ini")

    db.delete(comment)
    db.commit()

    return {"message": "Komentar berhasil dihapus"}