#!/bin/bash
set -e
# Run migrations
echo "Running database migrations..."
poetry run alembic upgrade head

# Start FastAPI
# Note: PYTHONPATH=/app/src allows imports like "main.app"
echo "Starting FastAPI application..."
poetry run uvicorn "main.app:create_application" \
    --factory \
    --host 0.0.0.0 \
    --port 8000
