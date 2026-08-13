from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlmodel import Session
from app.db.session import get_session
from app.schemas.user import UserCreate, UserRead
from app.services.user import create_user, delete_user, get_users

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})


def send_welcome_email(email: str) -> None:
    print(f"Sending welcome email to {email}")


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register(
    body: UserCreate,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    user = create_user(session, body)
    background_tasks.add_task(send_welcome_email, user.email)
    return user


@router.get(
    "/",
    response_model=list[UserRead],
)
def list(
    session: Session = Depends(get_session)
):
    return get_users(session)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    user_id: UUID,
    session: Session = Depends(get_session)
):
    return delete_user(session, user_id)