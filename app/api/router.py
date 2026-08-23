from fastapi import APIRouter

from app.api.routes.v1 import auth, users, workspaces
from app.api.routes import health

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(workspaces.router)