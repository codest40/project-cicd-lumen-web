#!/usr/bin/env bash
set -e

echo "Starting Flask Woeker App in production (Gunicorn WSGI worker)..."
exec gunicorn app:app \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers 4 \
  --timeout 120
