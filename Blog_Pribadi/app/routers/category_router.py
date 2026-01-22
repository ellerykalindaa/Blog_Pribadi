"""
Router ini menangani endpoint yang berkaitan dengan kategori
artikel blog.

Fitur:
- Menambahkan kategori baru
- Mengambil daftar kategori

Endpoint berada di bawah prefix '/categories'.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.database.models import Category
from app.schema.category_schema import CategoryCreate, CategoryResponse
from app.core.security import get_current_user

# =========================================================
# ROUTER CONFIGURATION
# =========================================================
router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

# =========================================================
# CREATE CATEGORY
# =========================================================
@router.post("/")
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Endpoint untuk membuat kategori baru.

    Endpoint ini hanya dapat diakses oleh user yang sudah login.

    Args:
        category (CategoryCreate): Data kategori baru.
        db (Session): Session database SQLAlchemy.
        user (User): User yang sedang login (hasil autentikasi).

    Returns:
        CategoryResponse: Data kategori yang berhasil dibuat.

    Raises:
        HTTPException: Jika kategori sudah ada.
    """
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Category already exists")

    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# =========================================================
# GET ALL CATEGORIES
# =========================================================
@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """
    Endpoint untuk mengambil seluruh kategori.

    Args:
        db (Session): Session database SQLAlchemy.

    Returns:
        list[CategoryResponse]: Daftar kategori.
    """
    return db.query(Category).all()