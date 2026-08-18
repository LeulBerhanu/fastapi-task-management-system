from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.exceptions import BadRequestError, NotFoundError
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate

async def create_user(async_session: AsyncSession, data: UserCreate) -> User:
    repo = UserRepository(async_session)

    if await repo.get_by_email(data.email):
        raise BadRequestError("Invalid Email or Password")

    user = User(email=data.email, hashed_password=await hash_password(data.password))
    user = await repo.create(user)

    await async_session.commit()
    await async_session.refresh(user)
    return user
    


async def get_users(async_session: AsyncSession) -> list[User]:
    repo = UserRepository(async_session)
    users = await repo.list()
    return users


async def get_user_by_email(async_session: AsyncSession, email: str) -> User | None:
    repo = UserRepository(async_session)
    user = await repo.get_by_email(email)
    return user if user else None


async def delete_user(async_session: AsyncSession, user_id: UUID) -> None:
    repo = UserRepository(async_session)
    
    if await repo.delete(user_id):
        await async_session.commit()
        return None
    else:
        raise NotFoundError("User not found")