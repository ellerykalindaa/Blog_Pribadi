"""
Module security.py

Modul ini bertanggung jawab untuk:
- Pengelolaan autentikasi berbasis JWT
- Enkripsi dan verifikasi kata sandi pengguna
- Pengambilan data user yang sedang login

Digunakan sebagai dependency pada endpoint yang membutuhkan autentikasi.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext

from app.database.db import get_db
from app.database.models import User

# =========================================================
# KONFIGURASI JWT
# =========================================================

"""
SECRET_KEY digunakan untuk proses enkripsi dan dekripsi JWT.
ALGORITHM menentukan algoritma enkripsi token.
"""
SECRET_KEY = "blog-secret-key"
ALGORITHM = "HS256"

# =========================================================
# KONFIGURASI PASSWORD HASHING
# =========================================================

"""
pwd_context digunakan untuk meng-hash dan memverifikasi kata sandi
menggunakan algoritma PBKDF2.
"""
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Skema autentikasi HTTP Bearer
security = HTTPBearer() 

# =========================================================
# FUNGSI TOKEN
# =========================================================

def create_access_token(data: dict):
    """
    Membuat JSON Web Token (JWT) untuk autentikasi pengguna.

    Token berisi data payload (contohnya user_id) dan waktu kedaluwarsa.

    Args:
        data (dict): Data yang akan disimpan di dalam token.

    Returns:
        str: Token JWT yang sudah dienkripsi.
    """
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(hours=1)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# =========================================================
# FUNGSI AUTENTIKASI USER
# =========================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Mengambil data user yang sedang login berdasarkan token JWT.

    Fungsi ini digunakan sebagai dependency pada endpoint yang
    membutuhkan autentikasi.

    Args:
        credentials (HTTPAuthorizationCredentials): Token JWT dari header Authorization.
        db (Session): Session database SQLAlchemy.

    Returns:
        User: Objek user yang berhasil diautentikasi.

    Raises:
        HTTPException: Jika token tidak valid atau user tidak ditemukan.
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(status_code=401, detail="Token invalid")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token invalid")

# =========================================================
# FUNGSI PASSWORD
# =========================================================

def hash_password(password: str):
    """
    Mengenkripsi kata sandi pengguna sebelum disimpan ke database.

    Args:
        password (str): Kata sandi asli dari pengguna.

    Returns:
        str: Kata sandi yang sudah di-hash.
    """
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """
    Memverifikasi kecocokan kata sandi dengan hash yang tersimpan.

    Args:
        plain (str): Kata sandi yang dimasukkan pengguna.
        hashed (str): Kata sandi yang tersimpan dalam bentuk hash.

    Returns:
        bool: True jika kata sandi cocok, False jika tidak.
    """
    return pwd_context.verify(plain, hashed)
