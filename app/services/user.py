from uuid import UUID
from sqlmodel import Session
from app.core.exceptions import BadRequestError, NotFoundError
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate

def create_user(session: Session, data: UserCreate) -> User:
    repo = UserRepository(session)

    if repo.get_by_email(data.email):
        raise BadRequestError("Invalid Email or Password")

    user = User(email=data.email, hashed_password=hash_password(data.password))
    user = repo.create(user)

    session.commit()
    session.refresh(user)
    return user
    


def get_users(session: Session) -> list[User]:
    repo = UserRepository(session)
    users = repo.list()
    return users


def get_user_by_email(session: Session, email: str) -> User | None:
    repo = UserRepository(session)
    user = repo.get_by_email(email)
    return user if user else None


def delete_user(session: Session, user_id: UUID) -> None:
    repo = UserRepository(session)
    
    if repo.delete(user_id):
        session.commit()
        return None
    else:
        raise NotFoundError("User not found")