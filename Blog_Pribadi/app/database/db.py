"""
Module db.py

Modul ini bertanggung jawab untuk:
- Mengatur koneksi database menggunakan SQLAlchemy
- Menyediakan session database
- Menyediakan Base class untuk ORM model

Digunakan sebagai dependency pada service dan router.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# =========================================================
# KONFIGURASI DATABASE
# =========================================================

"""
DATABASE_URL menentukan lokasi dan jenis database yang digunakan.
Pada project ini digunakan SQLite.
"""
DATABASE_URL = "sqlite:///./blog.db"

# =========================================================
# ENGINE DATABASE
# =========================================================

"""
Engine digunakan sebagai penghubung antara aplikasi dan database.
connect_args digunakan khusus untuk SQLite agar dapat digunakan
dalam lingkungan multithreading (FastAPI).
"""
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# =========================================================
# SESSION DATABASE
# =========================================================

"""
SessionLocal digunakan untuk membuat session database
yang akan digunakan pada setiap request.

autoflush=False agar commit dilakukan secara manual
"""
SessionLocal = sessionmaker(bind=engine, autoflush=False)

# =========================================================
# BASE MODEL
# =========================================================

"""
Base merupakan class dasar yang digunakan oleh seluruh model ORM.
"""
Base = declarative_base()

# =========================================================
# DEPENDENCY DATABASE
# =========================================================
def get_db():
    """
    Dependency untuk mendapatkan session database.

    Fungsi ini akan:
    - Membuka session database
    - Menyediakan session ke endpoint atau service
    - Menutup session setelah request selesai

    Yields:
        Session: Objek session SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
