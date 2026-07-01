#!/usr/bin/env bash
set -euo pipefail

HOST="${APP_HOST:-0.0.0.0}"
PORT="${APP_PORT:-8000}"
ENV="${APP_ENV:-dev}"
WORKERS="${APP_WORKERS:-4}"

echo "Starting app in [${ENV}] mode on ${HOST}:${PORT}"

if [ "$ENV" = "prod" ]; then
    exec uvicorn app.main:app \
        --host "$HOST" \
        --port "$PORT" \
        --workers "$WORKERS"
else
    exec uvicorn app.main:app \
        --host "$HOST" \
        --port "$PORT" \
        --reload
fi
