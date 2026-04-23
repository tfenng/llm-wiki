#!/usr/bin/env bash
# llmwiki — start a local HTTP server on 127.0.0.1:8765.
# Usage: ./serve.sh [--port N] [--host H] [--open]
set -eu
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
if [ -n "${VIRTUAL_ENV:-}" ] || [ -n "${CONDA_PREFIX:-}" ]; then
  PYTHON_BIN="python3"
elif [ -x "$SCRIPT_DIR/.venv/bin/python" ]; then
  PYTHON_BIN="$SCRIPT_DIR/.venv/bin/python"
else
  PYTHON_BIN="python3"
fi
exec "$PYTHON_BIN" -m llmwiki serve "$@"
