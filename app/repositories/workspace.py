from sqlmodel import Session
from app.models.workspace import Workspace, WorkspaceMember
from app.repositories.base import BaseRepository

class WorkspaceRepository(BaseRepository[Workspace]):
    def __init__(self, session: Session):
        super().__init__(session, Workspace)

class WorkspaceMemberRepository(BaseRepository[WorkspaceMember]):
    def __init__(self, session: Session):
        super().__init__(session, WorkspaceMember)