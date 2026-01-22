"""Repository helpers for `User` model.

This module contains small helper functions that encapsulate common
database operations on the `User` model. Keeping these operations in a
repository layer makes business logic in services/controllers simpler
and easier to test.
"""

from sqlalchemy.orm import Session
from app.database.models import User


def get_user_by_username(db: Session, username: str):
    """Return a User by `username` or None if not found.

    Args:
        db (Session): SQLAlchemy session
        username (str): Username to look up

    Returns:
        User | None
    """
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: User):
    """Persist a new `User` to the database.

    Commits the transaction and refreshes the instance so the caller
    receives populated fields (e.g. `id`).

    Args:
        db (Session): SQLAlchemy session
        user (User): User instance to persist

    Returns:
        User: Persisted user instance with generated fields filled
    """
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
