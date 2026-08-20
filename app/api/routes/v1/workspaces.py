from fastapi import APIRouter, status
from app.api.deps import CurrentUserDep, WorkspaceServiceDep
from app.schemas.workspace import WorkspaceCreate, WorkspaceRead


router = APIRouter(prefix="/v1/workspaces", tags=["workspaces"], responses={404: {"description": "Not found"}})

@router.get("/", response_model=list[WorkspaceRead])
async def list_workspaces(
    workspace_service: WorkspaceServiceDep,
):
    workspaces = await workspace_service.list_workspaces()
    return workspaces

@router.post("/", response_model=WorkspaceRead, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    body: WorkspaceCreate,
    workspace_service: WorkspaceServiceDep,
    current_user: CurrentUserDep,
):
    workspace = await workspace_service.create_workspace(body, current_user.id)
    return workspace