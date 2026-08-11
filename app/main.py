from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.db.session import engine
from app.api.router import api_router
from app.api.exception_handlers import register_exception_handlers

@asynccontextmanager
async def lifespan(_: FastAPI):
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("DB connection established")

    yield

    engine.dispose()
    print("DB connection closed")

app = FastAPI(lifespan=lifespan)

register_exception_handlers(app)

app.include_router(api_router, prefix="/api")