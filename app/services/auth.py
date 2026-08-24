from datetime import datetime, timezone
from app.core.exceptions import BadRequestError, UnauthorizedError
from app.core.security import create_access_token, generate_refresh_token, hash_refresh_token, verify_password
from app.db.uow import UnitOfWork
from app.models.refresh_token import RefreshToken


class AuthService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def login_user(self, email: str, password: str) -> dict[str, str]:
        user = await self.uow.users.get_by_email(email)
        
        if not user:
            raise BadRequestError("Invalid Email or Password")
        if not await verify_password(password, user.hashed_password):
            raise BadRequestError("Invalid Email or Password")
        
        access_token = create_access_token(user.id)
        raw_refresh_token, refresh_token_hash = generate_refresh_token()

        await self.uow.refresh_tokens.create(RefreshToken(
            user_id=user.id,
            token_hash=refresh_token_hash,
        ))
        await self.uow.commit()

        return { "access_token": access_token, "refresh_token": raw_refresh_token }

    
    async def refresh(self, raw: str) -> dict[str, str]:
        stored_refresh_token = await self._get_active_refresh_token(raw)
        await self.uow.refresh_tokens.revoke(stored_refresh_token)

        access_token = create_access_token(stored_refresh_token.user_id)
        new_raw, new_token_hash = generate_refresh_token()

        await self.uow.refresh_tokens.create(RefreshToken(
            user_id=stored_refresh_token.user_id,
            token_hash=new_token_hash,
        ))
        await self.uow.commit()

        return { "access_token": access_token, "refresh_token": new_raw }


    async def logout(self, raw: str) -> None:
        stored_refresh_token = await self._get_active_refresh_token(raw)
        await self.uow.refresh_tokens.revoke(stored_refresh_token)
        await self.uow.commit()
    

    async def _get_active_refresh_token(self, raw: str) -> RefreshToken:
        token_hash = hash_refresh_token(raw)
        stored_refresh_token = await self.uow.refresh_tokens.get_by_token_hash(token_hash)

        if (
            stored_refresh_token is None
            or stored_refresh_token.revoked
            or stored_refresh_token.expires_at < datetime.now(timezone.utc)
        ):
            raise UnauthorizedError("Invalid Refresh Token")
        return stored_refresh_token