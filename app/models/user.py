from datetime import datetime, timezone
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
from sqlalchemy import String, Boolean, DateTime

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(sa_type=String(255), unique=True, index=True, nullable=False)
    hashed_password: str = Field(sa_type=String(255), nullable=False)
    is_active: bool = Field(sa_type=Boolean, default=True)
    created_at: datetime = Field(sa_type=DateTime, default_factory=lambda: datetime.now(timezone.utc))