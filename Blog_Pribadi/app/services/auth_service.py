from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database.models import User
from app.core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status
from app.database.models import User
from app.core.security import create_access_token

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def register_user(db: Session, username: str, password: str):
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

def login_user(db: Session, username: str, password: str):
    print(" LOGIN USER DIPANGGIL ")
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        return None

    return create_access_token({"user_id": user.id})