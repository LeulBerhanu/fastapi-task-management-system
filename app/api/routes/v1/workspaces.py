from uuid import UUID
from fastapi import APIRouter, Path, status, Depends
from fastapi_pagination import Page
from app.api.deps import CurrentUserDep, WorkspaceServiceDep, get_current_user
from app.core.rbac import OwnerAccess
from app.schemas.workspace import WorkspaceCreate, WorkspaceMemberCreate, WorkspaceRead, WorkspaceWithMembersRead


router = APIRouter(prefix="/v1/workspaces", tags=["Workspaces"], dependencies=[Depends(get_current_user)], responses={404: {"description": "Not found"}})

@router.get("/", response_model=Page[WorkspaceRead])
async def list_workspaces(
    workspace_service: WorkspaceServiceDep,
):
    workspaces = await workspace_service.list_workspaces()
    return workspaces


@router.get("/{workspace_id}", response_model=WorkspaceWithMembersRead)
async def get_workspace(
    workspace_service: WorkspaceServiceDep,
    workspace_id: UUID = Path(...)
):
    workspace = await workspace_service.get_details(workspace_id)
    return workspace


@router.post("/", response_model=WorkspaceRead, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    body: WorkspaceCreate,
    workspace_service: WorkspaceServiceDep,
    current_user: CurrentUserDep,
):
    workspace = await workspace_service.create_workspace(body, current_user.id)
    return workspace

@router.post("/{workspace_id}/members", response_model=WorkspaceMemberCreate, status_code=status.HTTP_201_CREATED)
async def add_workspace_member(
    body: WorkspaceMemberCreate,
    workspace_service: WorkspaceServiceDep,
    membership: OwnerAccess,
    workspace_id: UUID = Path(...)
):
    workspace_member = await workspace_service.add_workspace_member(workspace_id, body)
    return workspace_member