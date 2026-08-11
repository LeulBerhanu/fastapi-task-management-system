from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlmodel import Session
from app.db.session import get_session
from app.schemas.user import UserCreate, UserCreateResponse, UserRead
from app.services.user import create_user, get_users, get_user_by_email
from app.core.exceptions import BadRequestError

router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})


def send_welcome_email(email: str) -> None:
    print(f"Sending welcome email to {email}")


@router.post(
    "/",
    response_model=UserCreateResponse,
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