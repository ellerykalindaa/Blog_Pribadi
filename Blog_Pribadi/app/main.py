from fastapi import FastAPI
from app.database.db import engine
from app.database import models
from app.routers import auth_router, post_router, category_router, comment_router


app = FastAPI(title="Blog Pribadi API")

app.include_router(auth_router.router)
app.include_router(category_router.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)