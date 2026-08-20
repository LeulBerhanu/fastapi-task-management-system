from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.session import get_async_session
from app.schemas.auth import Token
from app.services.auth import login_user

router = APIRouter(prefix="/v1/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSession = Depends(get_async_session)):
    return login_user(session, form_data.username, form_data.password)
     