#!/bin/bash
cd "$(dirname "$0")"
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
poetry run uvicorn src.main.app:create_application --factory --host 0.0.0.0 --port 8000

