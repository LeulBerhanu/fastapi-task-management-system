from uuid import UUID
from app.core.exceptions import NotFoundError
from app.db.uow import UnitOfWork
from app.schemas.task import TaskCreate
from app.models.task import Task

class TaskService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def list_tasks(self, workspace_id: UUID) -> list[Task] | []:
        tasks = await self.uow.tasks.list_by_workspace_id(workspace_id)
        return tasks or []

    async def create_task(self, task: TaskCreate, workspace_id: UUID) -> Task:
        task = Task(
            title=task.title,
            description=task.description,
            status=task.status,
            assignee_id=task.assignee_id,
            workspace_id=workspace_id
        )
        task = await self.uow.tasks.create(task)
        await self.uow.commit()
        return task

    async def get_task(self, task_id: UUID) -> Task:
        task = await self.uow.tasks.get_by_id(task_id)
        if task is None:
            raise NotFoundError("Task not found")
        return task