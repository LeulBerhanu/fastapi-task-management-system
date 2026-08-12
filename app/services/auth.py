

from sqlmodel import Session
from app.core.exceptions import BadRequestError
from app.core.security import create_access_token, verify_password
from app.schemas.auth import LoginRequest
from app.services.user import get_user_by_email


def login_user(session: Session, request: LoginRequest) -> dict[str, str]:
    user = get_user_by_email(session, request.email)
    
    if not user:
        raise BadRequestError("Invalid Email or Password")
    if not verify_password(request.password, user.hashed_password):
        raise BadRequestError("Invalid Email or Password")
    
    token = create_access_token(user.id)
    return {"access_token": token}