from enum import Enum
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, DateTime
from sqlmodel import SQLModel, Field, UniqueConstraint, Relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone

if TYPE_CHECKING:
    from app.models import User, Task, WorkspaceMember

class WorkspaceRole(str, Enum):
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"

class Workspace(SQLModel, table=True):
    __tablename__ = "workspaces"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(sa_type=String(255))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_type=DateTime(timezone=True))
    tasks: list["Task"] = Relationship(back_populates="workspace")
    members: list["WorkspaceMember"] = Relationship(back_populates="workspace")

class WorkspaceMember(SQLModel, table=True):
    __tablename__ = "workspace_members"
    __table_args__ = (UniqueConstraint("workspace_id", "user_id", name="uix_workspace_member"),)
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    workspace_id: UUID = Field(foreign_key="workspaces.id")
    workspace: Optional["Workspace"]  = Relationship(back_populates="members")
    user_id: UUID = Field(foreign_key="users.id")
    user: Optional["User"]  = Relationship(back_populates="memberships")
    role: WorkspaceRole = Field(max_length=20)
    joined_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_type=DateTime(timezone=True))