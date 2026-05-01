# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.5
FROM python:${PYTHON_VERSION}-slim as base

# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.5
FROM python:${PYTHON_VERSION}-slim as base

# Optimization and security settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV HOME=/tmp
ENV UV_CACHE_DIR=/tmp/.uv_cache

WORKDIR /app

# Install system dependencies (needed for psycopg2 and other packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-privileged user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/tmp" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Install uv for faster and more reliable dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Change ownership of the working directory to the non-privileged user
RUN chown appuser:appuser /app

# Switch to non-privileged user
USER appuser

# Copy only dependency files to leverage Docker cache
COPY --chown=appuser:appuser pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev --no-install-project

# Copy the rest of the application code
# We exclude files using .dockerignore
COPY --chown=appuser:appuser . .

# Expose the port (Cloud Run default)
EXPOSE 8080

# Production run command using uvicorn
# We use 8080 as requested in suggestion.txt
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
