from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database.models import User
from app.core.security import create_access_token

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def login_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        return None

    token = create_access_token({"user_id": user.id})
    return token
