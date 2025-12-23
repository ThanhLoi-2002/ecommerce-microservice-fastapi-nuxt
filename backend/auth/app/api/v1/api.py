from fastapi import APIRouter
from app.api.v1.routes import auth, user, media, category, size

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"], prefix="/auth")
api_router.include_router(user.router, tags=["users"], prefix="/users")
api_router.include_router(media.router, tags=["media"], prefix="/media")
api_router.include_router(category.router, tags=["categories"], prefix="/categories")
api_router.include_router(size.router, tags=["sizes"], prefix="/sizes")