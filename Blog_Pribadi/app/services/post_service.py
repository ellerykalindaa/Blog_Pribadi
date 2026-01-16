from app.database.models import Post
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import post_repository
from datetime import datetime

def build_post(data, user_id: int):
    return Post(
        title=data.title,
        content=data.content,
        category_id=data.category_id,
        user_id=user_id
    )

def get_posts(db: Session):
    return post_repository.get_all_posts(db)


def get_post_detail(db: Session, post_id: int):
    return post_repository.get_post_by_id(db, post_id)


def edit_post(db: Session, post_id: int, title: str, content: str, user_id: int):
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

print(" POST SERVICE LOADED ")

def create_post(db: Session, data, user_id: int):
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