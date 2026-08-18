from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.exceptions import BadRequestError, NotFoundError
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, session: AsyncSession, repo: UserRepository):
        self.session = session
        self.repo = repo

    async def create_user(self, data: UserCreate) -> User:
        if await self.repo.get_by_email(data.email):
            raise BadRequestError("Invalid Email or Password")

        user = User(email=data.email, hashed_password=await hash_password(data.password))
        user = await self.repo.create(user)

        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def get_user_by_id(self, user_id: UUID) -> User | None:
        user = await self.repo.get_by_id(user_id)
        return user if user else None


    async def get_users(self) -> list[User]:
        users = await self.repo.list()
        return users


    async def get_user_by_email(self, email: str) -> User | None:
        user = await self.repo.get_by_email(email)
        return user if user else None


    async def delete_user(self, user_id: UUID) -> None:
        if await self.repo.delete(user_id):
            await self.session.commit()
            return None
        else:
            raise NotFoundError("User not found")