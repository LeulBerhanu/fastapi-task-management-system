from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, Depends, Response, status
from app.api.deps import CurrentUserDep, TaskServiceDep
from app.core.rbac import ReadAccess, WriteAccess, OwnerAccess
from app.email import send_tasks_export_email
from app.schemas.task import TaskCreate, TaskRead, TaskSummary, TaskUpdate
from fastapi_pagination import Page, Params


collection_router = APIRouter(tags=["Tasks"], responses={404: {"description": "Not found"}})

@collection_router.get("/", response_model=Page[TaskRead])
async def list_tasks(
    task_service: TaskServiceDep,
    workspace_id: UUID,
    membership: ReadAccess,
    params: Params = Depends()
):
    tasks = await task_service.list_tasks(workspace_id, params)
    return tasks

@collection_router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    body: TaskCreate,
    task_service: TaskServiceDep,
    workspace_id: UUID,
    membership: WriteAccess,
):
    task = await task_service.create_task(body, workspace_id)
    return task

@collection_router.get("/summary", response_model=TaskSummary)
async def get_tasks_summary(
    workspace_id: UUID,
    task_service: TaskServiceDep,
    membership: ReadAccess,
):
    return await task_service.get_summary(workspace_id)

@collection_router.post("/export", status_code=status.HTTP_202_ACCEPTED)
async def export_tasks(
    workspace_id: UUID,
    background_tasks: BackgroundTasks,
    current_user: CurrentUserDep,
    membership: ReadAccess,
) -> Response:
    background_tasks.add_task(
        send_tasks_export_email,
        current_user.email,
        workspace_id,
    )
    return Response(status_code=status.HTTP_202_ACCEPTED)

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
    workspace_id: UUID,
    task_service: TaskServiceDep,
    membership: OwnerAccess,
):
    await task_service.delete_task(task_id, workspace_id)
    return None