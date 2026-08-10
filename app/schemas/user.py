from datetime import datetime, timezone
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4, max_length=100)

class UserCreateResponse(BaseModel):
    id: UUID
    email: EmailStr
    message: str = "User created successfully"