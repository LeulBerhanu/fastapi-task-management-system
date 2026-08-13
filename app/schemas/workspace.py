from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class WorkspaceCreate(BaseModel):
    name: str

class WorkspaceRead(BaseModel):
    id: UUID
    name: str
    created_at: datetime
