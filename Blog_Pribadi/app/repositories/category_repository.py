from sqlalchemy.orm import Session
from app.database.models import Category

def create_category(db: Session, category: Category):
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_categories(db: Session):
    return db.query(Category).all()
