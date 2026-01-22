from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database.models import User
from app.core.security import create_access_token

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(plain, hashed):
    """Memverifikasi password plain text dengan hash-nya.
    
    Args:
        plain (str): Password plain text
        hashed (str): Password yang sudah di-hash
        
    Returns:
        bool: True jika password cocok, False jika tidak
    """
    return pwd_context.verify(plain, hashed)

def login_user(db: Session, username: str, password: str):
    """Memverifikasi user login dan membuat token akses.
    
    Args:
        db (Session): Database session
        username (str): Username user
        password (str): Password user
        
    Returns:
        str: Access token jika login berhasil, None jika gagal
    """
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        return None

    return create_access_token({"user_id": user.id})

