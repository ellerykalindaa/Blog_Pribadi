"""
Modul ini berisi operasi database yang berkaitan dengan entitas Post.
Menggunakan Repository Pattern untuk memisahkan logika akses data
dari business logic.
"""

from sqlalchemy.orm import Session, joinedload
from app.database.models import Post


# =========================================================
# CREATE POST
# =========================================================

def create_post(db: Session, post: Post):
    """
    Menyimpan data post baru ke dalam database.

    Args:
        db (Session): Session database SQLAlchemy.
        post (Post): Objek Post yang akan disimpan.

    Returns:
        Post: Objek Post yang telah tersimpan.
    """
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

# =========================================================
# READ POST
# =========================================================

def get_all_posts(db: Session):
    """
    Mengambil seluruh data post dari database.

    Args:
        db (Session): Session database SQLAlchemy.

    Returns:
        list[Post]: Daftar seluruh post.
    """
    return (
        db.query(Post)
        .options(joinedload(Post.author))
        .all()
    )

def get_post_by_id(db: Session, post_id: int):
    """
    Mengambil satu data post berdasarkan ID.

    Args:
        db (Session): Session database SQLAlchemy.
        post_id (int): ID post.

    Returns:
        Post | None: Objek Post jika ditemukan, None jika tidak.
    """
    return db.query(Post).filter(Post.id == post_id).first()

# =========================================================
# UPDATE POST
# =========================================================

def update_post(db: Session, post: Post, title: str, content: str):
    """
    Memperbarui data post.

    Args:
        db (Session): Session database SQLAlchemy.
        post (Post): Objek Post yang akan diperbarui.
        title (str): Judul baru post.
        content (str): Konten baru post.

    Returns:
        Post: Objek Post yang telah diperbarui.
    """
    post.title = title
    post.content =  content
    db.commit()
    db.refresh(post)
    return post

# =========================================================
# DELETE POST
# =========================================================

def delete_post(db: Session, post: Post):
    """
    Menghapus data post dari database.

    Args:
        db (Session): Session database SQLAlchemy.
        post (Post): Objek Post yang akan dihapus.
    """
    db.delete(post)
    db.commit()
