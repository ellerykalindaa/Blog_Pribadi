from fastapi import FastAPI
from app.database.db import Base, engine
from app.database import models
from app.routers import auth_router, post_router, category_router, comment_router
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Blog Pribadi API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # untuk development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(category_router.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)