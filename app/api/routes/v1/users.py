from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, status
from app.schemas.user import UserCreate, UserRead
from app.api.deps import UserServiceDep
from app.email import send_welcome_email

router = APIRouter(prefix="/v1/users", tags=["Users"], responses={404: {"description": "Not found"}})


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    body: UserCreate,
    background_tasks: BackgroundTasks,
    user_service: UserServiceDep
):
    user = await user_service.create_user(body)
    background_tasks.add_task(send_welcome_email, user.email)
    return user


@router.get(
    "/",
    response_model=list[UserRead],
)
async def list(
    user_service: UserServiceDep
):
    users = await user_service.get_users()
    return users


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    user_id: UUID,
    user_service: UserServiceDep
):
    await user_service.delete_user(user_id)
    return None