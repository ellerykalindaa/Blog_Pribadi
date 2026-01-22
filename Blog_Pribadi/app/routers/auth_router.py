"""
Router ini menangani endpoint yang berkaitan dengan autentikasi
pengguna, meliputi:
- Registrasi user
- Login user
- Mengambil data user yang sedang login
- Logout user

Endpoint dalam router ini berada di bawah prefix '/auth'.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database.db import get_db
from app.database.models import User
from app.schema.user_schema import UserRegister, UserLogin
from app.services.auth_service import register_user, login_user
from app.core.security import get_current_user

# =========================================================
# ROUTER CONFIGURATION
# =========================================================

router = APIRouter(
    prefix="/auth", 
    tags=["Auth"]
)

# Context hashing password (digunakan saat registrasi)
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"], 
    deprecated="auto"
)

def hash_password(password: str):
    """
    Mengenkripsi password pengguna.

    Args:
        password (str): Password asli.

    Returns:
        str: Password yang telah di-hash.
    """
    return pwd_context.hash(password)

# =========================================================
# REGISTER USER
# =========================================================

@router.post("/register")
def register(data: UserRegister, db: Session = Depends(get_db)):
    """
    Endpoint untuk registrasi user baru.

    Args:
        data (UserRegister): Data registrasi user.
        db (Session): Session database SQLAlchemy.

    Returns:
        dict: Pesan keberhasilan registrasi.

    Raises:
        HTTPException: Jika username sudah digunakan.
    """
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(
            status_code=400, 
            detail="Username sudah digunakan"
        )

    user = User(
        username=data.username,
        password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    return {"message": "Registrasi berhasil"}

# =========================================================
# LOGIN USER
# =========================================================

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    """
    Endpoint untuk login user.

    Args:
        data (UserLogin): Data login user.
        db (Session): Session database SQLAlchemy.

    Returns:
        dict: Access token JWT dan tipe token.

    Raises:
        HTTPException: Jika username atau password salah.
    """
    token = login_user(db, data.username, data.password)

    if not token:
        raise HTTPException(
            status_code=401, 
            detail="Username atau password salah"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# =========================================================
# GET CURRENT USER
# =========================================================

@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    """
    Endpoint untuk mengambil data user yang sedang login.

    Args:
        current_user (User): User hasil autentikasi JWT.

    Returns:
        dict: Data user (id dan username).
    """
    return {
        "id": current_user.id,
        "username": current_user.username
    }
   
# =========================================================
# LOGOUT USER
# =========================================================

@router.post("/logout")
def logout():
    """
    Endpoint untuk logout user.

    Logout bersifat client-side dengan menghapus token
    yang tersimpan di sisi client.

    Returns:
        dict: Pesan logout.
    """
    return {"message": "Logout berhasil. Silakan hapus token di client."}
