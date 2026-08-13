

from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.api.deps import get_current_user
from app.db.session import get_session
from app.schemas.workspace import WorkspaceCreate, WorkspaceRead
from app.models.user import User
from app.services import workspace as workspace_service


router = APIRouter(prefix="/workspaces", tags=["workspaces"], responses={404: {"description": "Not found"}})

@router.get("/", response_model=list[WorkspaceRead])
def list_workspaces(
    session: Session = Depends(get_session),
):
    workspaces = workspace_service.list_workspaces(session)
    return workspaces

@router.post("/", response_model=WorkspaceRead, status_code=status.HTTP_201_CREATED)
def create_workspace(
    body: WorkspaceCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    workspace = workspace_service.create_workspace(session, body, current_user.id)
    return workspace