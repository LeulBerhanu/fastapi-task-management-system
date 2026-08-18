
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.user import User

from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, User)
    
    async def get_by_email(self, email: str) -> User | None:
        response = await self.async_session.exec(select(User).where(User.email == email))
        return response.one_or_none()