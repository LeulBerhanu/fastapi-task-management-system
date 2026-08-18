import asyncio
from datetime import datetime, timedelta, timezone
from uuid import UUID
from jose import JWTError, jwt
from pwdlib import PasswordHash
from app.core.config import settings
from app.core.exceptions import UnauthorizedError

password_hash = PasswordHash.recommended()

async def hash_password(password: str) -> str:
    hashed_password = await asyncio.to_thread(password_hash.hash, password)
    return hashed_password


async def verify_password(plain: str, hashed: str) -> bool:
    verified = await asyncio.to_thread(password_hash.verify, plain, hashed)
    return verified


def create_access_token(subject: UUID) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = jwt.encode(
        {"sub": str(subject), "exp": expire},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return access_token


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise UnauthorizedError("Invalid token")
        
    sub = payload.get("sub")
    if not sub:
        raise UnauthorizedError("Invalid token")
    return str(sub)