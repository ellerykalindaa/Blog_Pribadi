"""
Modul ini berisi business logic yang berkaitan dengan autentikasi user.
Digunakan untuk:
- Registrasi pengguna baru
- Login pengguna
- Validasi kredensial pengguna
- Pembuatan token JWT

Modul ini dipanggil oleh router auth (auth_router.py).
"""

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database.models import User
from app.core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status
from app.database.models import User
from app.core.security import create_access_token

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# =========================================================
# REGISTER USER
# =========================================================
def register_user(db: Session, username: str, password: str):
    """
    Mendaftarkan user baru ke dalam sistem.

    Fungsi ini akan:
    - Mengecek apakah username sudah terdaftar
    - Mengenkripsi password
    - Menyimpan data user ke database

    Args:
        db (Session): Session database SQLAlchemy.
        username (str): Username pengguna.
        password (str): Password pengguna.

    Returns:
        User: Objek user yang berhasil dibuat.

    Raises:
        HTTPException: Jika username sudah terdaftar.
    """
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    user = User(
        username=username,
        password=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# =========================================================
# LOGIN USER
# =========================================================
def login_user(db: Session, username: str, password: str):
    """
    Melakukan autentikasi pengguna (login).

    Fungsi ini akan:
    - Memverifikasi username dan password
    - Membuat token JWT jika kredensial valid

    Args:
        db (Session): Session database SQLAlchemy.
        username (str): Username pengguna.
        password (str): Password pengguna.

    Returns:
        str | None: Token JWT jika berhasil login,
        None jika username atau password salah.
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        return None

    return create_access_token({"user_id": user.id})