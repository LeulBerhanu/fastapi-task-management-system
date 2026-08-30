from datetime import datetime
from uuid import UUID
from app.core.exceptions import BadRequestError, NotFoundError
from app.db.uow import UnitOfWork
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.task import Task

class TaskService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def list_tasks(self, workspace_id: UUID) -> list[Task] | []:
        tasks = await self.uow.tasks.list_by_workspace_id(workspace_id)
        return tasks or []

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
        return updated_task

    async def delete_task(self, task_id: UUID, workspace_id: UUID) -> None:
        task = await self.uow.tasks.get_by_id(task_id)
        if task is None or task.workspace_id != workspace_id:
            raise NotFoundError("Task not found")

        deleted = await self.uow.tasks.delete(task_id)

        if not deleted:
            raise NotFoundError("Task not found")
            
        await self.uow.commit()