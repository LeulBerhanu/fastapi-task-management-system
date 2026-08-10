from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlmodel import Session
from app.db.session import get_session
from app.schemas.user import UserCreate, UserCreateResponse
from app.services.user import create_user, get_user_by_email


router = APIRouter(prefix="/users", tags=["users"], responses={404: {"description": "Not found"}})


def send_welcome_email(email: str) -> None:
    print(f"Sending welcome email to {email}")


@router.post(
    "/register",
    response_model=UserCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    body: UserCreate,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    if get_user_by_email(session, body.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Email or Password")

    user = create_user(session, body)
    background_tasks.add_task(send_welcome_email, user.email)

    return UserCreateResponse(id=user.id, email=user.email)