
from typing import Annotated
from uuid import UUID
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from app.core.exceptions import UnauthorizedError
from app.core.security import decode_access_token
from app.db.session import get_session
from app.models.user import User
from app.repositories.user import UserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(session: Annotated[Session, Depends(get_session)], token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    sub = decode_access_token(token)
    
    repo = UserRepository(session)
    user = repo.get_by_id(sub)

    if not user:
        raise UnauthorizedError("Invalid Token")
    return user
