from sqlalchemy.orm import selectinload
from sqlalchemy import func
from sqlmodel import select
from uuid import UUID
from app.models import Task
from app.models.task import TaskStatus
from app.repositories.base import BaseRepository
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi_pagination.ext.sqlmodel import apaginate
from fastapi_pagination import Page

class TaskRepository(BaseRepository[Task]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, Task)

    async def get_by_id(self, id: UUID) -> Task | None:
        task = await self.async_session.exec(
            select(Task).where(Task.id == id).options(selectinload(Task.assignee))
        )
        return task.one_or_none()

    async def list_by_workspace_id(self, workspace_id: UUID) -> Page[Task]:
        query = select(Task).where(Task.workspace_id == workspace_id).options(selectinload(Task.assignee)).order_by(Task.created_at.desc())
        return await apaginate(self.async_session, query)

    async def count_by_status(self, workspace_id: UUID) -> dict[TaskStatus, int]:
        result = await self.async_session.exec(
            select(Task.status, func.count(Task.id))
            .where(Task.workspace_id == workspace_id)
            .group_by(Task.status)
        )
        return {status: count for status, count in result.all()}