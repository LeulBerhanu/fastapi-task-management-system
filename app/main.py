from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text
from fastapi_pagination import add_pagination

from app.db.session import engine
from app.api.router import api_router
from app.api.exception_handlers import register_exception_handlers
from app.core.config import settings
from app.core.redis import redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
        print("DB connection established")
    
    app.state.redis = redis
    await app.state.redis.ping()
    print("Redis connection established")
    
    yield

    await app.state.redis.aclose()
    print("Redis connection closed")
    await engine.dispose()
    print("DB connection closed")

app = FastAPI(
    lifespan=lifespan,
    # docs_url=None if settings.is_production else "/docs",
    # redoc_url=None if settings.is_production else "/redoc",
)

register_exception_handlers(app)

app.include_router(api_router, prefix=settings.API_PREFIX)
add_pagination(app)