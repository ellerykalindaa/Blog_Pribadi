from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import Category
from app.schema.category_schema import CategoryCreate

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.get("/")
def get_all_categories(db: Session = Depends(get_db)):
    """
    Get semua kategori
    
    Returns:
        List[Category]: Daftar semua kategori
    """
    categories = db.query(Category).all()
    return categories

@router.post("/")
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db)
):
    """
    Create kategori baru
    
    Args:
        data: CategoryCreate schema dengan nama kategori
        db: Database session
        
    Returns:
        Category: Kategori yang baru dibuat
    """
