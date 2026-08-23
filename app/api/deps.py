from collections.abc import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.exceptions import NotFoundError
from app.core.security import decode_access_token
from app.db.session import get_async_session
from app.models.user import User
from app.services.user import UserService
from app.services.workspace import WorkspaceService
from app.db.uow import UnitOfWork
from app.services.auth import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]


async def get_uow(async_session: AsyncSessionDep) -> AsyncGenerator[UnitOfWork, None]:
    async with UnitOfWork(async_session) as uow:
        yield uow

UowDep = Annotated[UnitOfWork, Depends(get_uow)]


# Service Dependencies
def get_user_service(uow: UowDep) -> UserService:
    return UserService(uow)

def get_workspace_service(uow: UowDep) -> WorkspaceService:
    return WorkspaceService(uow)

def get_auth_service(uow: UowDep) -> AuthService:
    return AuthService(uow)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
WorkspaceServiceDep = Annotated[WorkspaceService, Depends(get_workspace_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], uow: UowDep) -> User:
    sub = decode_access_token(token)
    
    user = await uow.users.get_by_id(sub)

    if not user:
        raise NotFoundError("User not found")
    return user

CurrentUserDep = Annotated[User, Depends(get_current_user)]
