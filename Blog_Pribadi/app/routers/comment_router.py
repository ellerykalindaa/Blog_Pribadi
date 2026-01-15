from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import Comment, Post
from app.schema.comment_schema import CommentCreate
from app.core.security import get_current_user

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@router.post("/posts/{post_id}")
def add_comment(
    post_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Menambahkan komentar ke sebuah postingan blog.
    Hanya user yang sudah login yang dapat menambahkan komentar.
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
    return comment
