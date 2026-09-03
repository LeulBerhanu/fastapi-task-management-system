# Task Management API

Python 3.13+, PostgreSQL, [uv](https://docs.astral.sh/uv/).

## Run with Docker

```bash
cp .env.example .env
docker compose up --build
```

`.env.example` sets `POSTGRES_HOST=postgres` (the Compose service name). Leave that as-is for Docker.

Apply migrations:

```bash
docker compose exec api uv run alembic upgrade head
```

API: http://127.0.0.1:8000  
Docs: http://127.0.0.1:8000/docs

## Local setup

Copy `.env.example` to `.env` and set `POSTGRES_HOST=localhost`. Postgres must be running locally, or you can keep the Compose Postgres service and point the local app at `localhost:5432`.

```bash
uv sync
uv run alembic upgrade head
```

## Start the server

```bash
uv run fastapi dev
```

For production, staging, or test, create `.env.production`, `.env.staging`, or `.env.test` (copy from `.env.example` and adjust values), then start with that file:

```bash
uv run --env-file .env.production fastapi dev
uv run --env-file .env.staging fastapi dev
uv run --env-file .env.test fastapi dev
```

API: http://127.0.0.1:8000  
Docs: http://127.0.0.1:8000/docs
