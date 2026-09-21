FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependencies
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Copy the rest of the application
COPY . .

# Expose the port
EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT}"]