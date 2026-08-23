
from app.core.exceptions import BadRequestError
from app.core.security import create_access_token, verify_password
from app.db.uow import UnitOfWork


class AuthService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def login_user(self, email: str, password: str) -> dict[str, str]:
        user = await self.uow.users.get_by_email(email)
        
        if not user:
            raise BadRequestError("Invalid Email or Password")
        if not await verify_password(password, user.hashed_password):
            raise BadRequestError("Invalid Email or Password")
        
        token = create_access_token(user.id)

        return {"access_token": token}