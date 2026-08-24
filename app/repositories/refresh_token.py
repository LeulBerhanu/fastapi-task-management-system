from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, update
from datetime import datetime, timezone
from app.repositories.base import BaseRepository
from app.models.refresh_token import RefreshToken
from uuid import UUID

class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session, RefreshToken)

    async def get_by_token_hash(self, token_hash: str) -> RefreshToken | None:
        response = await self.async_session.exec(select(RefreshToken).where(RefreshToken.token_hash == token_hash))
        return response.one_or_none()

    async def revoke(self, token: RefreshToken) -> RefreshToken:
        token.revoked = True
        token.updated_at = datetime.now(timezone.utc)
        self.async_session.add(token)
        await self.async_session.flush()
        await self.async_session.refresh(token)
        return token

    async def revoke_all_for_user(self, user_id: UUID) -> None:
        await self.async_session.exec(
            update(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked == False,
            )
            .values(
                revoked=True,
                updated_at=datetime.now(timezone.utc),
            )
        )
        await self.async_session.flush()