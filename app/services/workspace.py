

from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.workspace import Workspace, WorkspaceMember, WorkspaceRole
from app.repositories.workspace import WorkspaceMemberRepository, WorkspaceRepository
from app.schemas.workspace import WorkspaceCreate


class WorkspaceService:
    def __init__(self, session: AsyncSession, workspace_repo: WorkspaceRepository, workspace_member_repo: WorkspaceMemberRepository):
        self.session = session
        self.workspace_repo = workspace_repo
        self.workspace_member_repo = workspace_member_repo

    async def list_workspaces(self) -> list[Workspace]:
        return await self.workspace_repo.list()

    async def create_workspace(self, data: WorkspaceCreate, user_id: UUID) -> Workspace:
        workspace = Workspace(name=data.name)
        workspace = await self.workspace_repo.create(workspace)

        member = WorkspaceMember(
            user_id=user_id, 
            workspace_id=workspace.id, 
            role=WorkspaceRole.OWNER
        )
        member = await self.workspace_member_repo.create(member)

        await self.session.commit()
        await self.session.refresh(workspace)
        await self.session.refresh(member)

        return workspace