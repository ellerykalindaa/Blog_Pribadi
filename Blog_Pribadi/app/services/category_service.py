"""
Modul ini berisi business logic sederhana yang berkaitan dengan
pembuatan objek Category.

Digunakan untuk memisahkan proses pembentukan model Category
dari layer router.
"""
from app.database.models import Category

def build_category(data):
    """
    Membuat objek Category dari data input.

    Fungsi ini biasanya dipanggil dari router sebelum data
    disimpan ke database.

    Args:
        data: Data input kategori (biasanya CategoryCreate schema).

    Returns:
        Category: Objek Category yang siap disimpan ke database.
    """
    return Category(name=data.name)
