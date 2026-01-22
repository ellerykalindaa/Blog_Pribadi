from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base


class User(Base):
    """
    Model User untuk menyimpan informasi pengguna.
    
    Attributes:
        id (int): Primary key, ID unik pengguna
        username (str): Nama pengguna, harus unik
        password (str): Password yang sudah di-hash
        posts (relationship): Relasi one-to-many dengan Post (posts yang dibuat user)
        comments (relationship): Relasi one-to-many dengan Comment (comments user)
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    posts = relationship(
        "Post",
        back_populates="author",
        foreign_keys="Post.author_id"
    )

    comments = relationship("Comment", back_populates="user")


class Post(Base):
    """
    Model Post untuk menyimpan artikel/postingan blog.
    
    Attributes:
        id (int): Primary key, ID unik postingan
        title (str): Judul postingan
        content (str): Isi/konten postingan
        created_at (datetime): Waktu pembuatan postingan
        author_id (int): Foreign key ke User (penulis postingan)
        category_id (int): Foreign key ke Category (kategori postingan)
        author (relationship): Relasi many-to-one dengan User
        comments (relationship): Relasi one-to-many dengan Comment
        category (relationship): Relasi many-to-one dengan Category
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))

    author = relationship(
        "User",
        back_populates="posts",
        foreign_keys=[author_id]
    )

    comments = relationship("Comment", back_populates="post")
    category = relationship("Category", back_populates="posts")


class Comment(Base):
    """
    Model Comment untuk menyimpan komentar pada postingan.
    
    Attributes:
        id (int): Primary key, ID unik komentar
        content (str): Isi/teks komentar
        created_at (datetime): Waktu pembuatan komentar
        user_id (int): Foreign key ke User (penulis komentar)
        post_id (int): Foreign key ke Post (postingan yang dikomentar)
        user (relationship): Relasi many-to-one dengan User
        post (relationship): Relasi many-to-one dengan Post
    """
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")


class Category(Base):
    """
    Model Category untuk menyimpan kategori postingan.
    
    Attributes:
        id (int): Primary key, ID unik kategori
        name (str): Nama kategori, harus unik
        posts (relationship): Relasi one-to-many dengan Post
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    posts = relationship("Post", back_populates="category")
