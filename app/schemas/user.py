from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
    created_at: datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4, max_length=100)

class UserCreateResponse(BaseModel):
    id: UUID
    email: EmailStr
    message: str = "User created successfully"
    created_at: datetime