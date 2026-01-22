"""
Modul ini bertanggung jawab untuk mengelola operasi database
yang berkaitan dengan entitas Category.

Layer repository berfungsi sebagai penghubung langsung antara
aplikasi dan database.
"""
from sqlalchemy.orm import Session
from app.database.models import Category

# =========================================================
# CREATE CATEGORY
# =========================================================
def create_category(db: Session, category: Category):
    """
    Menyimpan data kategori baru ke dalam database.

    Args:
        db (Session): Session database SQLAlchemy.
        category (Category): Objek Category yang akan disimpan.

    Returns:
        Category: Objek Category yang telah tersimpan di database.
    """
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

# =========================================================
# GET ALL CATEGORIES
# =========================================================
def get_categories(db: Session):
    """
    Mengambil seluruh data kategori dari database.

    Args:
        db (Session): Session database SQLAlchemy.

    Returns:
        list[Category]: Daftar seluruh kategori.
    """
    return db.query(Category).all()
