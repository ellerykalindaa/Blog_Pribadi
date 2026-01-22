"""Repository helpers for `Post` model operations.

Provides small, focused functions to create, read, update and delete
`Post` objects from the database. These helpers keep database code
centralized and reusable.
"""

from sqlalchemy.orm import Session
from app.database.models import Post


def create_post(db: Session, post: Post):
    """Persist a new `Post` instance to the database.

    Commits the transaction and refreshes the object so generated fields
    (e.g. `id`, `created_at`) are available to the caller.
    """
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_all_posts(db: Session):
    """Return a list of all Post records.

    Args:
        db (Session): SQLAlchemy session

    Returns:
        List[Post]
    """
    return db.query(Post).all()


def get_post_by_id(db: Session, post_id: int):
    """Return a Post by its ID or None if not found."""
    return db.query(Post).filter(Post.id == post_id).first()


def update_post(db: Session, post: Post):
    """Commit changes to a Post instance and refresh it."""
    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post: Post):
    """Delete a Post from the database and commit the transaction."""
    db.delete(post)
    db.commit()


def update_post(db: Session, post: Post, title: str, content: str):
    """Update title and content of a Post and persist changes.

    Note: this function intentionally updates fields and commits.
    """
    post.title = title
    post.content = content
    db.commit()
    db.refresh(post)
    return post