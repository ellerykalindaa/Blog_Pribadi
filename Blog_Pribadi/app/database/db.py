"""Database setup and helper for creating sessions.

This module defines the SQLAlchemy engine, session factory and base
declarative class used across the application.

Usage:
    from app.database.db import get_db
    db = next(get_db())  # or use as Depends(get_db) in FastAPI
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./blog.db"

# Create SQLAlchemy engine. `check_same_thread` is False to allow
# usage from different threads which is common in web servers.
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory used to create DB sessions
SessionLocal = sessionmaker(bind=engine, autoflush=False)
# Base class for ORM models
Base = declarative_base()


def get_db():
    """Yield a database session and ensure it is closed afterwards.

    This generator is intended to be used with FastAPI's dependency
    injection (Depends). It yields a SQLAlchemy `Session` and guarantees
    the session is closed whether the request succeeds or fails.

    Yields:
        Session: SQLAlchemy session instance
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
