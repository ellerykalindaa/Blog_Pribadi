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
    """Hash password menggunakan pbkdf2_sha256 algorithm.
    
    Args:
        password (str): Password plain text
        
    Returns:
        str: Password yang sudah di-hash
    """
    return pwd_context.hash(password)


@router.post("/register")
def register(data: UserRegister, db: Session = Depends(get_db)):
    """Register user baru.
    
    Args:
        data (UserRegister): Username dan password user baru
        db (Session): Database session
        
    Returns:
        dict: ID, username, dan message sukses
        
    Raises:
        HTTPException: 400 jika password > 72 karakter atau username sudah ada
    """
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

    return {
        "id": user.id,
        "username": user.username,
        "message": "Registrasi berhasil"
    }


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    """Login dengan username dan password.
    
    Args:
        data (UserLogin): Username dan password
        db (Session): Database session
        
    Returns:
        dict: Access token, token type, user ID, dan username
        
    Raises:
        HTTPException: 401 jika username atau password salah
    """
    user = db.query(User).filter(User.username == data.username).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Username atau password salah")
    
    # Verify password menggunakan auth_service
    from app.core.security import verify_password
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Username atau password salah")
    
    # Create token
    from app.core.security import create_access_token
    token = create_access_token({"user_id": user.id})
    
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username
    }

@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    """Get current authenticated user info.
    
    Args:
        current_user: User dari JWT token (via dependency)
        
    Returns:
        dict: ID dan username user yang sedang login
    """
    return {
        "id": current_user.id,
        "username": current_user.username
    }
   

@router.post("/logout")
def logout():
    """Logout user. 
    
    Pada JWT bersifat stateless, logout dilakukan di sisi client
    dengan menghapus token yang tersimpan.
    
    Returns:
        dict: Message logout berhasil
    """
    return {"message": "Logout berhasil. Silakan hapus token di client."}
