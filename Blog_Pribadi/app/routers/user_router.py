from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.db import get_db
from app.database.models import User
from app.schema.user_schema import UserResponse


"""Lightweight user endpoints used by the frontend.

This router provides simple read-only endpoints for listing users and
fetching a user by id. The endpoints are exposed both as `/users` and
as `/auth/users` to maintain compatibility with older frontend paths.
"""

router_users = APIRouter(prefix="/users", tags=["Users"])
router_auth_users = APIRouter(prefix="/auth/users", tags=["Users"])


def _serialize_user(user: User):
    """Return a compact serializable representation of a User.

    Args:
        user (User): ORM User instance

    Returns:
        dict: Dictionary with `id` and `username`
    """
    return {"id": user.id, "username": user.username}


@router_users.get("/", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    """Return all users in the system.

    Args:
        db (Session): Database session

    Returns:
        List[UserResponse]: All users as Pydantic response models
    """
    users = db.query(User).all()
    return [UserResponse(id=u.id, username=u.username) for u in users]


@router_users.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Return a single user by id.

    Raises HTTP 404 if the user does not exist.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(id=user.id, username=user.username)


# Mirror the same endpoints under /auth/users for compatibility with frontend
@router_auth_users.get("/", response_model=List[UserResponse])
def list_users_auth(db: Session = Depends(get_db)):
    """Alias for `/users/` exposed under `/auth/users/`.

    This preserves compatibility with frontend code that expects
    `/auth/users`.
    """
    return list_users(db)


@router_auth_users.get("/{user_id}", response_model=UserResponse)
def get_user_auth(user_id: int, db: Session = Depends(get_db)):
    """Alias for `/users/{id}` exposed under `/auth/users/{id}`."""
    return get_user(user_id, db)
