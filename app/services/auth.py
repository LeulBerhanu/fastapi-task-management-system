
from app.core.exceptions import BadRequestError
from app.core.security import create_access_token, verify_password
from app.api.deps import UserServiceDep


async def login_user(email: str, password: str, user_service: UserServiceDep) -> dict[str, str]:
    user = await user_service.get_user_by_email(email)
    
    if not user:
        raise BadRequestError("Invalid Email or Password")
    if not verify_password(password, user.hashed_password):
        raise BadRequestError("Invalid Email or Password")
    
    token = create_access_token(user.id)
    return {"access_token": token}