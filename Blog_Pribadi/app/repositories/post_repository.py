from sqlalchemy.orm import Session
from app.database.models import Post

def create_post(db: Session, post: Post):
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_all_posts(db: Session):
    return db.query(Post).all()

def get_post_by_id(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def update_post(db: Session, post: Post):
    db.commit()
    db.refresh(post)
    return post

def delete_post(db: Session, post: Post):
    db.delete(post)
    db.commit()

def update_post(db: Session, post: Post, title: str, content: str):
    post.title = title
    post.content = content
    db.commit()
    db.refresh(post)
    return post