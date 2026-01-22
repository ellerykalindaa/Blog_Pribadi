from pydantic import BaseModel

class UserRegister(BaseModel):
    """Schema untuk registrasi user baru.
    
    Attributes:
        username (str): Nama pengguna unik, max 50 karakter
        password (str): Password user, minimal 8 karakter
    """
    username: str
    password: str

class UserLogin(BaseModel):
    """Schema untuk login user.
    
    Attributes:
        username (str): Nama pengguna
        password (str): Password user
    """
    username: str
    password: str

class UserResponse(BaseModel):
    """Schema untuk respons data user.
    
    Attributes:
        id (int): ID unik user
        username (str): Nama pengguna
    
    Config:
        from_attributes: Mengizinkan konversi dari ORM objects
    """
    id: int
    username: str
    
    class Config:
        from_attributes = True
