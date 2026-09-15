from datetime import datetime
from uuid import UUID

from redis.asyncio import Redis
from app.core.exceptions import BadRequestError, NotFoundError
from app.db.uow import UnitOfWork
from app.schemas.task import TaskCreate, TaskRead, TaskSummary, TaskUpdate
from app.models.task import Task, TaskStatus
from fastapi_pagination import Page, Params

class TaskService:
    def __init__(self, uow: UnitOfWork, redis: Redis):
        self.uow = uow
        self.redis = redis

    async def _invalidate_workspace_tasks_cache(self, workspace_id: UUID) -> None:
        pattern = f"workspace:{workspace_id}:tasks:*"
        keys = [key async for key in self.redis.scan_iter(match=pattern)]
        if keys:
            await self.redis.delete(*keys)

    async def list_tasks(self, workspace_id: UUID, params: Params) -> Page[TaskRead]:
        cache_key = f"workspace:{workspace_id}:tasks:page:{params.page}:size:{params.size}"
        cached_tasks = await self.redis.get(cache_key)
        if cached_tasks:
            print("cache hit")
            return Page[TaskRead].model_validate_json(cached_tasks)

        page_result = await self.uow.tasks.list_by_workspace_id(workspace_id)
        payload = Page[TaskRead].model_validate(page_result).model_dump_json()
        await self.redis.set(cache_key, payload, ex=60)
        return page_result

    async def get_summary(self, workspace_id: UUID) -> TaskSummary:
        cache_key = f"workspace:{workspace_id}:tasks:summary"
        cached_summary = await self.redis.get(cache_key)
        if cached_summary:
            return TaskSummary.model_validate_json(cached_summary)

        counts = await self.uow.tasks.count_by_status(workspace_id)
        summary = TaskSummary(
            total=sum(counts.values()),
            pending=counts.get(TaskStatus.PENDING, 0),
            in_progress=counts.get(TaskStatus.IN_PROGRESS, 0),
            completed=counts.get(TaskStatus.COMPLETED, 0),
        )
        await self.redis.set(cache_key, summary.model_dump_json(), ex=300)
        return summary

    async def create_task(self, task: TaskCreate, workspace_id: UUID) -> Task:
        workspace = await self.uow.workspaces.get_by_id(workspace_id)
        if workspace is None:
            raise NotFoundError("Workspace not found")
        
        task = Task(
            **task.model_dump(),
            workspace_id=workspace_id
        )

        if task.assignee_id is not None:
            membership = await self.uow.workspace_members.get_membership(workspace_id, task.assignee_id)
            if membership is None:
                raise BadRequestError("Assignee must be a member of the workspace")
        
        task = await self.uow.tasks.create(task)
        await self.uow.commit()
        await self._invalidate_workspace_tasks_cache(workspace_id)
        return task

    async def get_task(self, task_id: UUID) -> Task:
        task = await self.uow.tasks.get_by_id(task_id)
        if task is None:
            raise NotFoundError("Task not found")
        return task

    async def update_task(self, task_id: UUID, workspace_id: UUID, data: TaskUpdate) -> Task:
        task = await self.uow.tasks.get_by_id(task_id)
        if task is None or task.workspace_id != workspace_id:
            raise NotFoundError("Task not found")

        data = data.model_dump(exclude_unset=True)
    
        if data.get("assignee_id") is not None:
            assignee_exists = await self.uow.workspace_members.get_membership(workspace_id, data.get("assignee_id"))
            if assignee_exists is None:
                raise BadRequestError("Assignee must be a member of the workspace")
        
        data["updated_at"] = datetime.now()

        updated_task = await self.uow.tasks.update(task_id, data)

        if updated_task is None:
            raise NotFoundError("Task not found")
            
        await self.uow.commit()
        await self._invalidate_workspace_tasks_cache(workspace_id)
        return updated_task

    async def delete_task(self, task_id: UUID, workspace_id: UUID) -> None:
        task = await self.uow.tasks.get_by_id(task_id)
        if task is None or task.workspace_id != workspace_id:
            raise NotFoundError("Task not found")

        deleted = await self.uow.tasks.delete(task_id)

        if not deleted:
            raise NotFoundError("Task not found")
            
        await self.uow.commit()
        await self._invalidate_workspace_tasks_cache(workspace_id)