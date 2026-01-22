"""Application entry point and router registration.

This module creates the FastAPI application, registers middleware and
includes routers. It also mounts the `frontend/` directory as static
files so that the single backend process can serve both the API and
the client files during development.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from app.database.db import Base, engine
from app.database import models
from app.routers import auth_router, post_router, category_router, comment_router, user_router
from fastapi.middleware.cors import CORSMiddleware


# Ensure DB tables exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ReelBlog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # untuk development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth_router.router)
app.include_router(category_router.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)
app.include_router(user_router.router_users)
app.include_router(user_router.router_auth_users)


# Serve static frontend files from /frontend
frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
if os.path.exists(frontend_path):
    app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")


@app.get("/")
async def root():
    """Serve the frontend index.html as the root route.

    If `frontend/index.html` exists it is returned as a FileResponse. This
    simplifies development because a single process serves both API and
    static client files.
    """
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Welcome to Blog API"}