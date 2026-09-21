from redis.asyncio import Redis
from app.core.config import settings

redis = Redis.from_url(
    settings.redis_url,
    encoding="utf-8",
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5
)