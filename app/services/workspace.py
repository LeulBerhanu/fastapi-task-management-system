from uuid import UUID
from app.core.exceptions import BadRequestError, NotFoundError
from app.models.workspace import Workspace, WorkspaceMember, WorkspaceRole
from app.schemas.workspace import WorkspaceCreate, WorkspaceMemberCreate
from app.db.uow import UnitOfWork


class WorkspaceService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    # TODO: setup pagination and sorting for list endpoints

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

    async def get_by_id(self, workspace_id: UUID) -> Workspace:
        workspace = await self.uow.workspaces.get_by_id(workspace_id)
        if workspace is None:
            raise NotFoundError("Workspace not found")
        return workspace

    async def get_details(self, workspace_id: UUID) -> Workspace:
        workspace = await self.uow.workspaces.get_details(workspace_id)
        if workspace is None:
            raise NotFoundError("Workspace not found")
        return workspace

    async def add_workspace_member(self, workspace_id: UUID, data: WorkspaceMemberCreate) -> WorkspaceMember:
        if data.role == WorkspaceRole.OWNER:
            raise BadRequestError("Owner role cannot be assigned to a user")
        
        user = await self.uow.users.get_by_id(data.user_id)
        if user is None:
            raise NotFoundError("User not found")

        membership = await self.uow.workspace_members.get_membership(workspace_id, data.user_id)
        if membership is not None:
            raise BadRequestError("User is already a member of the workspace")

        member = WorkspaceMember(
            user_id=data.user_id,
            workspace_id=workspace_id,
            role=data.role
        )

        member = await self.uow.workspace_members.create(member)

        await self.uow.commit()

        return member

    # TODO: Add list members endpoint