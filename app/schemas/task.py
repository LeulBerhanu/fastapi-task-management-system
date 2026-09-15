from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from app.models.task import TaskStatus
from app.schemas.user import UserRead

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    assignee_id: UUID | None = None

class TaskRead(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    assignee: UserRead | None = None
    workspace_id: UUID
    created_at: datetime
    updated_at: datetime

class TaskSummary(BaseModel):
    total: int
    pending: int
    in_progress: int
    completed: int

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    assignee_id: UUID | None = None