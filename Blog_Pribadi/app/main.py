"""
Main application entry point.

File ini berfungsi sebagai titik masuk (entry point) aplikasi FastAPI
untuk sistem Blog Pribadi.

Tanggung jawab utama file ini:
- Inisialisasi aplikasi FastAPI
- Inisialisasi koneksi dan tabel database
- Konfigurasi middleware (CORS)
- Mendaftarkan seluruh router aplikasi
"""
from fastapi import FastAPI
from app.database.db import Base, engine
from app.database import models
from app.routers import auth_router, post_router, category_router, comment_router
from fastapi.middleware.cors import CORSMiddleware

# =========================================================
# DATABASE INITIALIZATION
# =========================================================
# Membuat seluruh tabel database berdasarkan model SQLAlchemy
Base.metadata.create_all(bind=engine)

# =========================================================
# FASTAPI APPLICATION
# =========================================================
app = FastAPI(title="Blog Pribadi API")

# =========================================================
# MIDDLEWARE CONFIGURATION
# =========================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # untuk development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# ROUTER REGISTRATION
# =========================================================
app.include_router(auth_router.router)
app.include_router(category_router.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)