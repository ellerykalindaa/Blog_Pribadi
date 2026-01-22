from app.database.models import Post, User
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import post_repository
from datetime import datetime
from app.schema.post_schema import PostResponse

def build_post(data, user_id: int):
    """Membuat object Post dari data input.
    
    Args:
        data: Data postingan (PostCreate)
        user_id (int): ID user yang membuat postingan
        
    Returns:
        Post: Object Post yang belum disimpan ke database
    """
    return Post(
        title=data.title,
        content=data.content,
        category_id=data.category_id,
        author_id=user_id
    )

def get_posts(db: Session):
    """Mengambil semua postingan beserta informasi penulis.
    
    Args:
        db (Session): Database session
        
    Returns:
        List[PostResponse]: Daftar semua postingan dengan username penulis
    """
    # JOIN DENGAN BENAR MENGGUNAKAN author_id
    posts = db.query(
        Post,
        User.username
    ).join(
        User, Post.author_id == User.id
    ).all()
    
    result = []
    for post, username in posts:
        post_data = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at,
            "author_id": post.author_id,
            "username": username,
            "category_id": post.category_id
        }
        result.append(PostResponse(**post_data))
    
    return result

def get_post_detail(db: Session, post_id: int):
    """Mengambil detail satu postingan beserta informasi penulis.
    
    Args:
        db (Session): Database session
        post_id (int): ID postingan
        
    Returns:
        PostResponse: Detail postingan atau None jika tidak ditemukan
    """
    result = db.query(
        Post,
        User.username
    ).join(
        User, Post.author_id == User.id
    ).filter(
        Post.id == post_id
    ).first()
    
    if not result:
        return None
    
    post, username = result
    
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        created_at=post.created_at,
        author_id=post.author_id,
        username=username,
        category_id=post.category_id
    )

def edit_post(db: Session, post_id: int, title: str, content: str, user_id: int):
    """Mengedit postingan (hanya untuk pemilik).
    
    Args:
        db (Session): Database session
        post_id (int): ID postingan yang akan diedit
        title (str): Judul baru
        content (str): Konten baru
        user_id (int): ID user yang mengedit
        
    Returns:
        Post: Object Post yang sudah diupdate atau None jika tidak ditemukan
        
    Raises:
        HTTPException: 403 jika user bukan pemilik postingan
    """
    post = post_repository.get_post_by_id(db, post_id)
    if not post:
        return None

    if post.author_id != user_id:
        raise HTTPException(status_code=403, detail="Tidak diizinkan")

    post.title = title
    post.content = content
    db.commit()
    db.refresh(post)
    return post

def create_post(db: Session, data, user_id: int):
    """Membuat postingan blog baru.
    
    Args:
        db (Session): Database session
        data: Data postingan (PostCreate)
        user_id (int): ID user yang membuat postingan
        
    Returns:
        Post: Object Post yang baru dibuat
    """
    post = Post(
        title=data.title,
        content=data.content,
        author_id=user_id,
        category_id=data.category_id,
        created_at=datetime.utcnow()
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post