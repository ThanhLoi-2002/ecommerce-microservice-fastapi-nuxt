from fastapi import APIRouter
from app.api.v1.routes import auth, user, media

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"], prefix="/auth")
api_router.include_router(user.router, tags=["user"], prefix="/user")
api_router.include_router(media.router, tags=["media"], prefix="/media")