from enum import Enum
from sqlalchemy import String
from sqlmodel import SQLModel, Field, UniqueConstraint
from uuid import UUID, uuid4
from datetime import datetime, timezone

class WorkspaceRole(str, Enum):
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"

class Workspace(SQLModel, table=True):
    __tablename__ = "workspaces"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(sa_type=String(255))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class WorkspaceMember(SQLModel, table=True):
    __tablename__ = "workspace_members"
    __table_args__ = (UniqueConstraint("workspace_id", "user_id", name="uix_workspace_member"),)
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    workspace_id: UUID = Field(foreign_key="workspaces.id")
    user_id: UUID = Field(foreign_key="users.id")
    role: WorkspaceRole = Field(max_length=20)
    joined_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))