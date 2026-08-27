from app.models.workspace import WorkspaceRole
from app.api.deps import UowDep, CurrentUserDep
from app.core.exceptions import ForbiddenError, NotFoundError

from fastapi import Path
from uuid import UUID

def RequireRole(*allowed_roles: WorkspaceRole):
    async def check_role(
        current_user: CurrentUserDep,
        uow: UowDep,
        workspace_id: UUID = Path(...)
    ):
        workspace = await uow.workspaces.get_by_id(workspace_id)
        if workspace is None:
            raise NotFoundError("Workspace not found")
    
        membership = await uow.workspace_members.get_membership(workspace_id, current_user.id)
        if not membership:
            raise ForbiddenError("You are not a member of this workspace")
        if membership.role not in allowed_roles:
            raise ForbiddenError("You are not authorized to access this resource")
        return membership

    return check_role