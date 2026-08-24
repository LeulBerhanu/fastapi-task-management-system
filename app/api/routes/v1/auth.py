from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import RefreshTokenRequest, Token
from app.api.deps import AuthServiceDep

router = APIRouter(prefix="/v1/auth", tags=["auth"])

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], auth_service: AuthServiceDep):
    return await auth_service.login_user(form_data.username, form_data.password)
     
@router.post("/refresh", response_model=Token, status_code=status.HTTP_200_OK)
async def refresh(body: RefreshTokenRequest, auth_service: AuthServiceDep):
    return await auth_service.refresh(body.refresh_token)

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(body: RefreshTokenRequest, auth_service: AuthServiceDep):
    await auth_service.logout(body.refresh_token)
