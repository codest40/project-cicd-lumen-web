#!/usr/bin/env bash
set -e

echo "Starting API App in production mode (Gunicorn + UvicornWorker)..."
exec gunicorn app:app \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers 4 \
  -k uvicorn.workers.UvicornWorker \
  --timeout 60
