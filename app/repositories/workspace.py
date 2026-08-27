from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.workspace import Workspace, WorkspaceMember
from app.repositories.base import BaseRepository
from uuid import UUID
from sqlmodel import select

class WorkspaceRepository(BaseRepository[Workspace]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, Workspace)

class WorkspaceMemberRepository(BaseRepository[WorkspaceMember]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, WorkspaceMember)

    async def get_membership(self, workspace_id: UUID, user_id: UUID) -> WorkspaceMember | None:
        query = select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id
        )
        result = await self.async_session.exec(query)
        return result.one_or_none()