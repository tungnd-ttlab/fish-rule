#!/bin/bash
set -e

# Load env
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

# Set PYTHONPATH (already set in Dockerfile, but ensure it's set)
export PYTHONPATH="${PYTHONPATH:-/app}"

# Wait for PostgreSQL to be ready (simple check)
# Docker Compose healthcheck should handle this, but adding extra safety
wait_for_postgres() {
    local host="${POSTGRES_HOST:-postgres}"
    local port="${POSTGRES_PORT:-5432}"
    local max_attempts=30
    local attempt=1

    echo "Waiting for PostgreSQL at ${host}:${port} to be ready..."
    
    # Check if pg_isready is available (from postgresql-client)
    if command -v pg_isready >/dev/null 2>&1; then
        while [ $attempt -le $max_attempts ]; do
            if pg_isready -h "${host}" -p "${port}" -U "${POSTGRES_USER:-postgres}" >/dev/null 2>&1; then
                echo "PostgreSQL is ready!"
                return 0
            fi
            echo "Attempt ${attempt}/${max_attempts}: PostgreSQL is not ready yet. Waiting..."
            sleep 2
            attempt=$((attempt + 1))
        done
    else
        # Fallback: simple TCP connection check
        while [ $attempt -le $max_attempts ]; do
            if timeout 2 bash -c "echo > /dev/tcp/${host}/${port}" 2>/dev/null; then
                echo "PostgreSQL port is open, assuming ready..."
                sleep 1
                return 0
            fi
            echo "Attempt ${attempt}/${max_attempts}: PostgreSQL is not ready yet. Waiting..."
            sleep 2
            attempt=$((attempt + 1))
        done
    fi
    
    echo "WARNING: Could not verify PostgreSQL readiness, but continuing anyway..."
}

# Wait for PostgreSQL (optional, docker-compose healthcheck should handle this)
wait_for_postgres || true

# Run migrations
echo "Running database migrations..."
poetry run alembic upgrade head

# Start FastAPI
# Note: PYTHONPATH=/app allows imports like "src.main.app"
echo "Starting FastAPI application..."
poetry run uvicorn "src.main.app:create_application" \
    --factory \
    --host 0.0.0.0 \
    --port 8000
