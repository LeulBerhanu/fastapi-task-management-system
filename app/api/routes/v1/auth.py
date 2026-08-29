from typing import Annotated
from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import RefreshTokenRequest, Token
from app.api.deps import AuthServiceDep
from app.schemas.user import UserCreate, UserRead
from app.core.email import send_welcome_email

router = APIRouter(prefix="/v1/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(body: UserCreate, background_tasks: BackgroundTasks, auth_service: AuthServiceDep):
    user = await auth_service.register_user(body)
    background_tasks.add_task(send_welcome_email, user.email)
    return user
    
@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], auth_service: AuthServiceDep):
    return await auth_service.login_user(form_data.username, form_data.password)
     
@router.post("/refresh", response_model=Token, status_code=status.HTTP_200_OK)
async def refresh(body: RefreshTokenRequest, auth_service: AuthServiceDep):
    return await auth_service.refresh(body.refresh_token)

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(body: RefreshTokenRequest, auth_service: AuthServiceDep):
    await auth_service.logout(body.refresh_token)
