from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import Category
from app.schema.category_schema import CategoryCreate
from app.core.security import get_current_user

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.post("/")
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(400, "Category already exists")

    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()
