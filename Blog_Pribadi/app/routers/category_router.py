from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import Category
from app.schema.category_schema import CategoryCreate

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.post("/")
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db)
):
    category = Category(name=data.name)  # ✅ BENAR
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
