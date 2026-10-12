FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.11.16 /uv /uvx /bin/

WORKDIR /app

# Native libraries required by Django's PostGIS/GEOS integration.
RUN apt-get update \
    && apt-get install -y --no-install-recommends libgdal36 libgeos3.13.1 \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first for layer caching
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=config.settings \
    PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
