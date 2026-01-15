from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database.db import get_db
from app.database.models import User
from app.schema.user_schema import UserRegister, UserLogin
from app.services.auth_service import login_user
from app.core.security import get_current_user


router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


@router.post("/register")
def register(data: UserRegister, db: Session = Depends(get_db)):
    if len(data.password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password maksimal 72 karakter"
        )

    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username sudah digunakan")

    user = User(
        username=data.username,
        password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "Registrasi berhasil"}


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    token = login_user(db, data.username, data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Username atau password salah")

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username
    }
   

@router.post("/logout")
def logout():
    """
    Logout user. Pada JWT bersifat stateless, logout dilakukan di sisi client
    dengan menghapus token yang tersimpan.
    """
    return {"message": "Logout berhasil. Silakan hapus token di client."}
