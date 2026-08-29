from uuid import UUID
from fastapi import APIRouter, status
from app.api.deps import TaskServiceDep
from app.core.rbac import ReadAccess, WriteAccess, OwnerAccess
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate


collection_router = APIRouter(tags=["Tasks"], responses={404: {"description": "Not found"}})

@collection_router.get("/", response_model=list[TaskRead])
async def list_tasks(
    task_service: TaskServiceDep,
    workspace_id: UUID,
    membership: ReadAccess,
):
    tasks = await task_service.list_tasks(workspace_id)
    return tasks or []

@collection_router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    body: TaskCreate,
    task_service: TaskServiceDep,
    workspace_id: UUID,
    membership: WriteAccess,
):
    task = await task_service.create_task(body, workspace_id)
    return task

@collection_router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: UUID,
    task_service: TaskServiceDep,
    membership: ReadAccess,
):
    task = await task_service.get_task(task_id)
    return task

@collection_router.patch("/{task_id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
async def update_task(
    task_id: UUID,
    workspace_id: UUID,
    body: TaskUpdate,
    task_service: TaskServiceDep,
    membership: WriteAccess,
):
    task = await task_service.update_task(task_id, workspace_id, body)
    return task

@collection_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    task_service: TaskServiceDep,
    membership: OwnerAccess,
):
    await task_service.delete_task(task_id)
    return None