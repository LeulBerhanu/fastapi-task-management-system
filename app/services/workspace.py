from uuid import UUID
from app.models.workspace import Workspace, WorkspaceMember, WorkspaceRole
from app.schemas.workspace import WorkspaceCreate
from app.db.uow import UnitOfWork


class WorkspaceService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def list_workspaces(self) -> list[Workspace]:
        return await self.uow.workspaces.list()

    async def create_workspace(self, data: WorkspaceCreate, user_id: UUID) -> Workspace:
        workspace = Workspace(name=data.name)
        workspace = await self.uow.workspaces.create(workspace)

        member = WorkspaceMember(
            user_id=user_id, 
            workspace_id=workspace.id, 
            role=WorkspaceRole.OWNER
        )
        member = await self.uow.workspace_members.create(member)

        await self.uow.commit()

        return workspace