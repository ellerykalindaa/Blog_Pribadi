from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext

from app.database.db import get_db
from app.database.models import User

SECRET_KEY = "blog-secret-key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
security = HTTPBearer() 

def create_access_token(data: dict):
    """Membuat JWT access token.
    
    Args:
        data (dict): Data untuk di-encode dalam token (harus berisi user_id)
        
    Returns:
        str: JWT token yang sudah di-encode dengan expiration 1 jam
    """
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(hours=1)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Mendapatkan user yang sedang authenticated dari JWT token.
    
    Args:
        credentials: HTTP Bearer token dari header Authorization
        db (Session): Database session
        
    Returns:
        User: Object User dari database
        
    Raises:
        HTTPException: 401 jika token tidak valid atau user tidak ditemukan
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
        raise HTTPException(status_code=401, detail="Token invalid")
    
def hash_password(password: str):
    """Hash password menggunakan pbkdf2_sha256.
    
    Args:
        password (str): Password plain text
        
    Returns:
        str: Password yang sudah di-hash
    """
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    """Memverifikasi password plain text dengan hash-nya.
    
    Args:
        plain (str): Password plain text
        hashed (str): Password yang sudah di-hash
        
    Returns:
        bool: True jika password cocok, False jika tidak
    """
    return pwd_context.verify(plain, hashed)
