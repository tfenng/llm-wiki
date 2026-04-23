#!/usr/bin/env bash
# llmwiki — build the static HTML site.
# Usage: ./build.sh [--synthesize] [--out <dir>]
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
exec "$PYTHON_BIN" -m llmwiki build "$@"
