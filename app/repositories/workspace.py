from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.workspace import Workspace, WorkspaceMember
from app.repositories.base import BaseRepository
from uuid import UUID
from sqlmodel import select

class WorkspaceRepository(BaseRepository[Workspace]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, Workspace)

    async def get_details(self, id: UUID) -> Workspace | None:
        query = select(Workspace).where(Workspace.id == id).options(selectinload(Workspace.members).selectinload(WorkspaceMember.user), selectinload(Workspace.tasks))
        result = await self.async_session.exec(query)
        return result.one_or_none()

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