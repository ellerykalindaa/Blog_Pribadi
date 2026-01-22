"""Repository helpers for `Category` model.

Simple helpers to create and list categories in the database.
"""

from sqlalchemy.orm import Session
from app.database.models import Category


def create_category(db: Session, category: Category):
    """Persist a new Category and return the created instance."""
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_categories(db: Session):
    """Return all Category records."""
    return db.query(Category).all()
