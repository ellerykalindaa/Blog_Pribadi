from pydantic import BaseModel

class CategoryCreate(BaseModel):
    """Schema untuk membuat kategori baru.
    
    Attributes:
        name (str): Nama kategori unik, max 100 karakter
    """
    name: str

class CategoryResponse(BaseModel):
    """Schema untuk respons data kategori.
    
    Attributes:
        id (int): ID unik kategori
        name (str): Nama kategori
    
    Config:
        from_attributes: Mengizinkan konversi dari ORM objects
    """
    id: int
    name: str
    
    class Config:
        from_attributes = True
