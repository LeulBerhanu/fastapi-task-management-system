from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.schemas.auth import LoginRequest, Token
from app.services.auth import login_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(request: LoginRequest, session: Session = Depends(get_session)):
    return login_user(session, request)
     