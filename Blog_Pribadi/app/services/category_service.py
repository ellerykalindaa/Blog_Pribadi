from app.database.models import Category

def build_category(data):
    return Category(name=data.name)
