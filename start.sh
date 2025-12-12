#!/usr/bin/env bash
set -euo pipefail

# Activate virtual environment if Railway created one
if [ -d "venv" ]; then
  source venv/bin/activate
elif [ -d ".venv" ]; then
  source .venv/bin/activate
fi

# Ensure backend sources are importable as "src"
export PYTHONPATH="$(pwd)/backend:${PYTHONPATH:-}"

# Launch FastAPI backend via Uvicorn
exec uvicorn backend.main:app --host 0.0.0.0 --port "${PORT:-8080}"
