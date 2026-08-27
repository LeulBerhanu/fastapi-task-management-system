from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, status
from app.api.deps import TaskServiceDep
from app.core.rbac import RequireRole
from app.models.workspace import WorkspaceMember, WorkspaceRole
from app.schemas.task import TaskCreate, TaskRead


collection_router = APIRouter(tags=["tasks"], responses={404: {"description": "Not found"}})

@collection_router.get("/", response_model=list[TaskRead])
async def list_tasks(
    task_service: TaskServiceDep,
    workspace_id: UUID,
    membership: Annotated[WorkspaceMember, Depends(RequireRole(WorkspaceRole.OWNER, WorkspaceRole.EDITOR, WorkspaceRole.VIEWER))],
):
    tasks = await task_service.list_tasks(workspace_id)
    return tasks or []

@collection_router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    body: TaskCreate,
    task_service: TaskServiceDep,
    workspace_id: UUID,
    membership: Annotated[WorkspaceMember, Depends(RequireRole(WorkspaceRole.OWNER, WorkspaceRole.EDITOR))]
):
    task = await task_service.create_task(body, workspace_id)
    return task


item_router = APIRouter(prefix="/v1/tasks", tags=["tasks"], responses={404: {"description": "Not found"}})

@item_router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: UUID,
    task_service: TaskServiceDep,
    membership: Annotated[WorkspaceMember, Depends(RequireRole(WorkspaceRole.OWNER, WorkspaceRole.EDITOR, WorkspaceRole.VIEWER))]
):
    task = await task_service.get_task(task_id)
    return task

# @item_router.put("/{task_id}", response_model=TaskRead)
# async def update_task(
#     task_id: UUID,
#     body: TaskUpdate,
#     task_service: TaskServiceDep,
#     membership: Annotated[WorkspaceMember, Depends(RequireRole(WorkspaceRole.OWNER, WorkspaceRole.EDITOR))]
# ):
#     task = await task_service.update_task(task_id, body)
#     return task