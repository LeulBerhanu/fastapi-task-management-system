from sqlmodel import Session, select
from app.core.security import hash_password
from app.models.user import User

def create_user(session: Session, user: User) -> User:
    user = User(email=user.email, hashed_password=hash_password(user.password))
    session.add(user)
    print("user added", user)
    session.commit()
    print("user committed", user)
    session.refresh(user)
    print("user refreshed", user)
    return user


def get_user_by_email(session: Session, email: str) -> User:
    return session.exec(select(User).where(User.email == email)).first()