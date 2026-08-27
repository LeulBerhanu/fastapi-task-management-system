from fastapi import APIRouter

from app.api.routes.v1 import auth, tasks, users, workspaces
from app.api.routes import health


api_router = APIRouter()

workspaces.router.include_router(
    tasks.collection_router, 
    prefix="/{workspace_id}/tasks")

api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(tasks.item_router)
api_router.include_router(users.router)
api_router.include_router(workspaces.router)
