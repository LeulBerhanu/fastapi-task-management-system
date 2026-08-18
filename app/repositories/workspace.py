from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.workspace import Workspace, WorkspaceMember
from app.repositories.base import BaseRepository

class WorkspaceRepository(BaseRepository[Workspace]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, Workspace)

class WorkspaceMemberRepository(BaseRepository[WorkspaceMember]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, WorkspaceMember)