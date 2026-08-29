from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel
from app.models.workspace import WorkspaceRole
from app.schemas.user import UserRead

class WorkspaceCreate(BaseModel):
    name: str

class WorkspaceRead(BaseModel):
    id: UUID
    name: str
    created_at: datetime

class WorkspaceMemberRead(BaseModel):
    id: UUID
    user_id: UUID
    role: WorkspaceRole
    joined_at: datetime
    user: UserRead

class WorkspaceWithMembersRead(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    members: list[WorkspaceMemberRead]

class WorkspaceMemberCreate(BaseModel):
    user_id: UUID
    role: Literal[WorkspaceRole.VIEWER, WorkspaceRole.EDITOR]