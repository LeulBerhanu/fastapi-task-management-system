from sqlalchemy.orm import selectinload
from sqlmodel import select
from uuid import UUID
from app.models import Task
from app.repositories.base import BaseRepository
from sqlmodel.ext.asyncio.session import AsyncSession

class TaskRepository(BaseRepository[Task]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, Task)

    async def get_by_id(self, id: UUID) -> Task | None:
        task = await self.async_session.exec(
            select(Task).where(Task.id == id).options(selectinload(Task.assignee))
        )
        return task.one_or_none()

    async def list_by_workspace_id(self, workspace_id: UUID) -> list[Task] | []:
        tasks = await self.async_session.exec(
            select(Task).where(Task.workspace_id == workspace_id).options(selectinload(Task.assignee)).order_by(Task.created_at.desc())
        )

        return tasks or []