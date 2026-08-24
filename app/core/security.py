import asyncio
from datetime import datetime, timedelta, timezone
import hashlib
import secrets
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
        settings.JWT_SECRET_KEY,
        algorithm=settings.HASH_ALGORITHM,
    )
    return access_token


def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.HASH_ALGORITHM]
        )
    except JWTError:
        raise UnauthorizedError("Invalid token")
        
    sub = payload.get("sub")
    if not sub:
        raise UnauthorizedError("Invalid token")
    return str(sub)


def generate_refresh_token() -> tuple[str, str]:
    raw = secrets.token_urlsafe(32)

    hashed = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    
    return raw, hashed

def hash_refresh_token(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()
