from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import Token
from app.api.deps import AuthServiceDep

router = APIRouter(prefix="/v1/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], auth_service: AuthServiceDep):
    return await auth_service.login_user(form_data.username, form_data.password)
     