from types import TracebackType
from sqlmodel.ext.asyncio.session import AsyncSession
from app.repositories.user import UserRepository
from app.repositories.workspace import WorkspaceMemberRepository, WorkspaceRepository


class UnitOfWork:
    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session
        self.users = UserRepository(async_session)
        self.workspaces = WorkspaceRepository(async_session)
        self.workspace_members = WorkspaceMemberRepository(async_session)

    async def commit(self):
        await self.async_session.commit()

    async def rollback(self):
        await self.async_session.rollback()

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            await self.rollback()