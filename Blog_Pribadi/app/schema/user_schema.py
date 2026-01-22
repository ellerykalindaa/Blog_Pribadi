"""
Modul ini berisi definisi schema Pydantic untuk entitas User.
Digunakan untuk:
- Validasi data registrasi pengguna
- Validasi data login pengguna

Schema ini digunakan pada endpoint autentikasi (auth).
"""
from pydantic import BaseModel, ConfigDict

class UserRegister(BaseModel):
    """
    Schema untuk registrasi pengguna baru.

    Digunakan sebagai request body pada endpoint:
    POST /auth/register
    """
    username: str
    password: str

class UserLogin(BaseModel):
    """
    Schema untuk login pengguna.

    Digunakan sebagai request body pada endpoint:
    POST /auth/login
    """
    username: str
    password: str

class AuthorResponse(BaseModel):
    """
    Schema ringkas untuk menampilkan author posting.
    """
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)