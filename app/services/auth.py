from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.core.exceptions import BadRequestError
from app.core.security import create_access_token, verify_password
from app.services.user import get_user_by_email


def login_user(session: Session, email: str, password: str) -> dict[str, str]:
    user = get_user_by_email(session, email)
    
    if not user:
        raise BadRequestError("Invalid Email or Password")
    if not verify_password(password, user.hashed_password):
        raise BadRequestError("Invalid Email or Password")
    
    token = create_access_token(user.id)
    return {"access_token": token}