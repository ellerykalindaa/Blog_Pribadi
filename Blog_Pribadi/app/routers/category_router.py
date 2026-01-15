from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schema.category_schema import CategoryCreate
from app.database.db import get_db
from app.repositories.category_repository import create_category, get_categories
from app.services.category_service import build_category

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/")
def create_category_api(data: CategoryCreate, db: Session = Depends(get_db)):
    category = build_category(data)
    return create_category(db, category)

@router.get("/")
def list_categories(db: Session = Depends(get_db)):
    return get_categories(db)
