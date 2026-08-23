from uuid import UUID
from app.core.exceptions import BadRequestError, NotFoundError
from app.core.security import hash_password
from app.db.uow import UnitOfWork
from app.models.user import User
from app.schemas.user import UserCreate


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_user(self, data: UserCreate) -> User:
        if await self.uow.users.get_by_email(data.email):
            raise BadRequestError("Invalid Email or Password")

        user = User(
            email=data.email, 
            hashed_password=await hash_password(data.password)
            )
        user = await self.uow.users.create(user)

        await self.uow.commit()
        return user
    
    async def get_user_by_id(self, user_id: UUID) -> User | None:
        user = await self.uow.users.get_by_id(user_id)
        return user if user else None


    async def get_users(self) -> list[User]:
        users = await self.uow.users.list()
        return users


    async def get_user_by_email(self, email: str) -> User | None:
        user = await self.uow.users.get_by_email(email)
        return user if user else None


    async def delete_user(self, user_id: UUID) -> None:
        if await self.uow.users.delete(user_id):
            await self.uow.commit()
            return None
        else:
            raise NotFoundError("User not found") 