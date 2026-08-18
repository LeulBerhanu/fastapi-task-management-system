from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.exceptions import NotFoundError
from app.core.security import decode_access_token
from app.db.session import get_async_session
from app.models.user import User
from app.repositories.user import UserRepository
from app.repositories.workspace import WorkspaceRepository, WorkspaceMemberRepository
from app.services.user import UserService
from app.services.workspace import WorkspaceService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]

# Repository Dependencies
def get_user_repository(session: AsyncSessionDep) -> UserRepository:
    return UserRepository(session)

def get_workspace_repository(session: AsyncSessionDep) -> WorkspaceRepository:
    return WorkspaceRepository(session)

def get_workspace_member_repository(session: AsyncSessionDep) -> WorkspaceMemberRepository:
    return WorkspaceMemberRepository(session)

UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
WorkspaceRepositoryDep = Annotated[WorkspaceRepository, Depends(get_workspace_repository)]
WorkspaceMemberRepositoryDep = Annotated[WorkspaceMemberRepository, Depends(get_workspace_member_repository)]

# Service Dependencies
def get_user_service(
    session: AsyncSessionDep,
    repo: UserRepositoryDep
) -> UserService:
    return UserService(session, repo)

def get_workspace_service(
    session: AsyncSessionDep,
    workspace_repo: WorkspaceRepositoryDep,
    workspace_member_repo: WorkspaceMemberRepositoryDep
) -> WorkspaceService:
    return WorkspaceService(session, workspace_repo, workspace_member_repo)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
WorkspaceServiceDep = Annotated[WorkspaceService, Depends(get_workspace_service)]

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], repo: UserRepositoryDep) -> User:
    sub = decode_access_token(token)
    
    user = await repo.get_by_id(sub)

    if not user:
        raise NotFoundError("User not found")
    return user

CurrentUserDep = Annotated[User, Depends(get_current_user)]