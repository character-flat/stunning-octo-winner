from fastapi import APIRouter

from app.api.endpoints import auth, notes, users

api_router = APIRouter(prefix="/api/v1")

# Include all endpoint routers
api_router.include_router(auth.router)
api_router.include_router(notes.router)
api_router.include_router(users.router)
