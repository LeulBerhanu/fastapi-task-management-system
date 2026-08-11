from typing import List
from sqlmodel import Session, select
from app.models.user import User
from uuid import UUID

from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(session, User)
    
    def get_by_email(self, email: str) -> User | None:
        return self.session.exec(select(User).where(User.email == email)).one_or_none()