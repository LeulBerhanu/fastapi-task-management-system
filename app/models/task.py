from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import DateTime, String
from datetime import datetime, timezone
from uuid import UUID
from uuid import uuid4
from enum import Enum

if TYPE_CHECKING:
    from app.models import User, Workspace

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(sa_type=String(255), nullable=False)
    description: str | None = Field(sa_type=String(255), nullable=True)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_type=DateTime(timezone=True))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_type=DateTime(timezone=True))
    workspace_id: UUID = Field(foreign_key="workspaces.id")
    workspace: Optional["Workspace"]  = Relationship(back_populates="tasks")
    assignee_id: UUID | None = Field(foreign_key="users.id", nullable=True)
    assignee: Optional["User"]  = Relationship(back_populates="tasks")