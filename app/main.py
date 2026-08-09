from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.db.session import engine

@asynccontextmanager
async def lifespan(_: FastAPI):
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("DB connection established")

    yield

    engine.dispose()
    print("DB connection closed")

app = FastAPI(lifespan=lifespan)