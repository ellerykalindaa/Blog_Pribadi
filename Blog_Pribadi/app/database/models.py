"""
Module models.py

Modul ini berisi definisi ORM (Object Relational Mapping)
untuk seluruh tabel database pada aplikasi Blog Pribadi.

Setiap class merepresentasikan satu tabel database dan
menggunakan SQLAlchemy ORM.
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

# =========================================================
# MODEL USER
# =========================================================

class User(Base):
    """
    Model User

    Merepresentasikan tabel 'users' yang menyimpan data pengguna
    aplikasi blog.

    Relasi:
    - One-to-Many dengan Post
    - One-to-Many dengan Comment
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    # Relasi ke tabel posts (1 user memiliki banyak post)
    posts = relationship(
        "Post",
        back_populates="author",
        foreign_keys="Post.author_id"
    )

    # Relasi ke tabel comments (1 user memiliki banyak comment)
    comments = relationship("Comment", back_populates="user")


# =========================================================
# MODEL POST
# =========================================================

class Post(Base):
    """
    Model Post

    Merepresentasikan tabel 'posts' yang menyimpan artikel blog.

    Relasi:
    - Many-to-One dengan User (author)
    - Many-to-One dengan Category
    - One-to-Many dengan Comment
    """

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))

    # Relasi ke tabel users sebagai penulis
    author = relationship(
        "User",
        back_populates="posts",
        foreign_keys=[author_id]
    )

    # Relasi ke tabel comments
    comments = relationship("Comment", back_populates="post")
    # Relasi ke tabel categories
    category = relationship("Category", back_populates="posts")

# =========================================================
# MODEL COMMENT
# =========================================================

class Comment(Base):
    """
    Model Comment

    Merepresentasikan tabel 'comments' yang menyimpan komentar
    pada setiap post.

    Relasi:
    - Many-to-One dengan User
    - Many-to-One dengan Post
    """

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

    # Relasi ke tabel users
    user = relationship("User", back_populates="comments")
    # Relasi ke tabel posts
    post = relationship("Post", back_populates="comments")


# =========================================================
# MODEL CATEGORY
# =========================================================

class Category(Base):
    """
    Model Category

    Merepresentasikan tabel 'categories' yang menyimpan kategori
    artikel blog.

    Relasi:
    - One-to-Many dengan Post
    """

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    # Relasi ke tabel posts
    posts = relationship("Post", back_populates="category")
