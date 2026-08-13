

from uuid import UUID
from sqlmodel import Session
from app.models.workspace import Workspace, WorkspaceMember, WorkspaceRole
from app.repositories.workspace import WorkspaceMemberRepository, WorkspaceRepository
from app.schemas.workspace import WorkspaceCreate

def list_workspaces(session: Session) -> list[Workspace]:
    repo = WorkspaceRepository(session)
    return repo.list()

def create_workspace(session: Session, data: WorkspaceCreate, user_id: UUID) -> Workspace:
    repo = WorkspaceRepository(session)
    member_repo = WorkspaceMemberRepository(session)
       
    workspace = Workspace(name=data.name)
    workspace = repo.create(workspace)

    member = WorkspaceMember(
        user_id=user_id, 
        workspace_id=workspace.id, 
        role=WorkspaceRole.OWNER
    )
    member_repo.create(member)

    session.commit()
    session.refresh(workspace)
    session.refresh(member)

    return workspace