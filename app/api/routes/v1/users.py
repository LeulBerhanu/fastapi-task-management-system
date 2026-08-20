from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, status
from app.schemas.user import UserCreate, UserRead
from app.api.deps import UserServiceDep

router = APIRouter(prefix="/v1/users", tags=["users"], responses={404: {"description": "Not found"}})


def send_welcome_email(email: str) -> None:
    print(f"Sending welcome email to {email}")


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register(
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