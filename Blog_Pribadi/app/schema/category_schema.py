"""
Modul ini berisi definisi schema Pydantic untuk entitas Category.
Digunakan untuk:
- Validasi data input dari client
- Menentukan format response API

Schema ini digunakan pada endpoint kategori (categories).
"""
from pydantic import BaseModel, ConfigDict

class CategoryBase(BaseModel):
    """
    Schema dasar untuk kategori.

    Class ini berfungsi sebagai schema induk (base schema)
    yang menyimpan field umum pada kategori.
    """
    name: str

class CategoryCreate(CategoryBase):
    """
    Schema untuk membuat kategori baru.

    Digunakan sebagai request body pada endpoint:
    POST /categories

    Mewarisi seluruh field dari CategoryBase.
    """
    pass

class CategoryResponse(CategoryBase):
    """
    Schema response kategori.

    Digunakan untuk mengembalikan data kategori ke client,
    termasuk ID kategori yang dihasilkan oleh database.
    """
    id: int

    # Mengizinkan Pydantic membaca data dari ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)