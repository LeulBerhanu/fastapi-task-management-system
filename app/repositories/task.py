from sqlalchemy import select
from uuid import UUID
from app.models import Task
from app.repositories.base import BaseRepository
from sqlmodel.ext.asyncio.session import AsyncSession

class TaskRepository(BaseRepository[Task]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, Task)

    async def list_by_workspace_id(self, workspace_id: UUID) -> list[Task] | []:
        result = await self.async_session.exec(
            select(Task).where(Task.workspace_id == workspace_id).order_by(Task.created_at.desc())
        )
        return result.all() if result.all() else []