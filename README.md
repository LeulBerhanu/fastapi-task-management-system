# Task Management API

Python 3.13+, PostgreSQL, [uv](https://docs.astral.sh/uv/).

## Setup

```bash
uv sync
uv run alembic upgrade head
```

## Start the server

```bash
uv run fastapi dev
```

API: http://127.0.0.1:8000  
Docs: http://127.0.0.1:8000/docs
