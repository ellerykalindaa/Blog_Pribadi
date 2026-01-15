from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class User(Base):
    """
    Model User untuk menyimpan data pengguna.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="user")


class Post(Base):
    """
    Model Post untuk menyimpan postingan blog.
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    category = relationship("Category", back_populates="posts")


class Comment(Base):
    """
    Model Comment untuk komentar pada postingan.
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
    Model Category untuk mengelompokkan postingan blog.
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    posts = relationship("Post", back_populates="category")
