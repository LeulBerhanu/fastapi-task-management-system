from sqlmodel import Session, select
from app.core.exceptions import BadRequestError, NotFoundError
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserCreateResponse, UserRead

def create_user(session: Session, data: UserCreate) -> UserCreateResponse:
    repo = UserRepository(session)

    if repo.get_by_email(data.email):
        raise BadRequestError("Invalid Email or Password")

    user = User(email=data.email, hashed_password=hash_password(data.password))
    user = repo.create(user)
    return UserCreateResponse.model_validate(user, from_attributes=True)


def get_users(session: Session) -> list[UserRead]:
    repo = UserRepository(session)
    users = repo.list()
    return [UserRead.model_validate(user, from_attributes=True) for user in users]


def get_user_by_email(session: Session, email: str) -> UserRead:
    repo = UserRepository(session)
    user = repo.get_by_email(email)
    if user is None:
        raise NotFoundError("User not found")
    return UserRead.model_validate(user, from_attributes=True)