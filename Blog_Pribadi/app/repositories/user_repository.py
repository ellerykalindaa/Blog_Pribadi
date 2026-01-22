"""
Modul ini bertanggung jawab untuk mengelola operasi database
yang berkaitan dengan entitas User.

Menggunakan Repository Pattern untuk memisahkan logika akses data
dari business logic.
"""
from sqlalchemy.orm import Session
from app.database.models import User

# =========================================================
# GET USER BY USERNAME
# =========================================================

def get_user_by_username(db: Session, username: str):
    """
    Mengambil data user berdasarkan username.

    Args:
        db (Session): Session database SQLAlchemy.
        username (str): Username yang dicari.

    Returns:
        User | None: Objek User jika ditemukan, None jika tidak.
    """
    return db.query(User).filter(User.username == username).first()

# =========================================================
# CREATE USER
# =========================================================

def create_user(db: Session, user: User):
    """
    Menyimpan data user baru ke dalam database.

    Args:
        db (Session): Session database SQLAlchemy.
        user (User): Objek User yang akan disimpan.

    Returns:
        User: Objek User yang telah tersimpan.
    """
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
