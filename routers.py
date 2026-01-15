from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from . import schemas, services, dependencies
from .database import get_db

# Auth router
auth_router = APIRouter()

@auth_router.post("/register", response_model=schemas.Token)
def register(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    auth_service = services.AuthService(db)
    return auth_service.register_user(user_data)

@auth_router.post("/login", response_model=schemas.Token)
def login(
    login_data: schemas.UserLogin,
    db: Session = Depends(get_db)
):
    auth_service = services.AuthService(db)
    return auth_service.login_user(login_data)

# Posts router
posts_router = APIRouter()

@posts_router.get("/", response_model=List[schemas.PostResponse])
def get_posts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Optional[schemas.UserResponse] = Depends(dependencies.get_current_user)
):
    user_id = current_user.id if current_user else None
    post_service = services.PostService(db)
    return post_service.get_all_posts(skip, limit, user_id)

@posts_router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[schemas.UserResponse] = Depends(dependencies.get_current_user)
):
    user_id = current_user.id if current_user else None
    post_service = services.PostService(db)
    return post_service.get_post_by_id(post_id, user_id)

def get_my_posts(
    current_user: schemas.UserResponse = Depends(dependencies.get_current_user),
    db: Session = Depends(get_db)
):
    post_service = services.PostService(db)
    return post_service.get_user_posts(current_user.id)

@posts_router.post("/", response_model=schemas.PostResponse)
def create_post(
    post_data: schemas.PostCreate,
    current_user: schemas.UserResponse = Depends(dependencies.get_current_user),
    db: Session = Depends(get_db)
):
    post_service = services.PostService(db)
    return post_service.create_post(post_data, current_user.id)

@posts_router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(
    post_id: int,
    post_update: schemas.PostUpdate,
    current_user: schemas.UserResponse = Depends(dependencies.get_current_user),
    db: Session = Depends(get_db)
):
    post_service = services.PostService(db)
    return post_service.update_post(post_id, post_update, current_user.id)

@posts_router.delete("/{post_id}")
def delete_post(
    post_id: int,
    current_user: schemas.UserResponse = Depends(dependencies.get_current_user),
    db: Session = Depends(get_db)
):
    post_service = services.PostService(db)
    return post_service.delete_post(post_id, current_user.id)

# Comments router
comments_router = APIRouter()

@comments_router.post("/", response_model=schemas.CommentResponse)
def create_comment(
    comment_data: schemas.CommentCreate,
    current_user: schemas.UserResponse = Depends(dependencies.get_current_user),
    db: Session = Depends(get_db)
):
    comment_service = services.CommentService(db)
    return comment_service.create_comment(comment_data, current_user.id)

@comments_router.get("/post/{post_id}", response_model=List[schemas.CommentResponse])
def get_post_comments(
    post_id: int,
    db: Session = Depends(get_db)
):
    comment_service = services.CommentService(db)
    return comment_service.get_comments_by_post(post_id)

@comments_router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    current_user: schemas.UserResponse = Depends(dependencies.get_current_user),
    db: Session = Depends(get_db)
):
    comment_service = services.CommentService(db)
    return comment_service.delete_comment(comment_id, current_user.id)

# Likes router (under posts)
@posts_router.post("/{post_id}/like")
def like_post(
    post_id: int,
    current_user: schemas.UserResponse = Depends(dependencies.get_current_user),
    db: Session = Depends(get_db)
):
    like_service = services.LikeService(db)
    return like_service.like_post(post_id, current_user.id)

@posts_router.delete("/{post_id}/like")
def unlike_post(
    post_id: int,
    current_user: schemas.UserResponse = Depends(dependencies.get_current_user),
    db: Session = Depends(get_db)
):
    like_service = services.LikeService(db)
    return like_service.unlike_post(post_id, current_user.id)

@posts_router.get("/", response_model=List[schemas.PostResponse])
def get_posts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Optional[schemas.UserResponse] = Depends(dependencies.get_current_user)
):
    user_id = current_user.id if current_user else None
    post_service = services.PostService(db)
    return post_service.get_all_posts(skip, limit, user_id)

# Users router (tambahkan di routers.py)
users_router = APIRouter()

@users_router.get("/me/posts", response_model=List[schemas.PostResponse])
def get_my_posts(
    current_user: schemas.UserResponse = Depends(dependencies.get_current_user),
    db: Session = Depends(get_db)
):
    post_service = services.PostService(db)
    return post_service.get_user_posts(current_user.id)