#!/usr/bin/env bash
# llmwiki — one-click installer for macOS / Linux.
#
# Usage: ./setup.sh
# Idempotent — safe to re-run.

set -eu
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "==> llmwiki setup"
echo "    root: $SCRIPT_DIR"

# 1. Python check
if ! command -v python3 >/dev/null 2>&1; then
  echo "error: python3 is required but was not found in PATH" >&2
  exit 1
fi
PY_VER=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "    python: $PY_VER"

# 2. Use the active virtualenv/conda env when present. Otherwise create a
#    local .venv so Homebrew / PEP 668 system Pythons still get a working
#    install without requiring global pip changes.
if [ -n "${VIRTUAL_ENV:-}" ] || [ -n "${CONDA_PREFIX:-}" ]; then
  PYTHON_BIN="python3"
else
  PYTHON_BIN="$SCRIPT_DIR/.venv/bin/python"
  if [ ! -x "$PYTHON_BIN" ]; then
    echo "==> creating local virtualenv (.venv)"
    python3 -m venv "$SCRIPT_DIR/.venv"
  fi
fi

# 3. Install runtime + build tooling inside the chosen environment.
export PIP_DISABLE_PIP_VERSION_CHECK=1

echo "==> installing llmwiki build/runtime deps"
"$PYTHON_BIN" -m pip install --quiet "setuptools>=82.0.1" wheel markdown
echo "==> installing llmwiki (-e .)"
"$PYTHON_BIN" -m pip install --quiet --no-build-isolation -e .
"$PYTHON_BIN" -c "import llmwiki, markdown"

# 4. Scaffold raw/ wiki/ site/
"$PYTHON_BIN" -m llmwiki init

# 5. Show available adapters
"$PYTHON_BIN" -m llmwiki adapters

# 6. Show current sync status so users can see what's ready.
echo
echo "==> current sync status:"
"$PYTHON_BIN" -m llmwiki sync --status --recent 5 || true

echo
echo "================================================================"
echo "  Setup complete."
echo "================================================================"
echo
echo "Next steps:"
echo "  ./sync.sh                   # convert new sessions to markdown"
echo "  ./build.sh                  # generate the static HTML site"
echo "  ./serve.sh                  # browse at http://127.0.0.1:8765/"
echo
echo "Optional SessionStart hook — auto-sync on every Claude Code launch:"
echo "  Add this to ~/.claude/settings.json under 'hooks':"
echo '    "SessionStart": [ { "hooks": [ { "type": "command",'
echo "      \"command\": \"($SCRIPT_DIR/sync.sh > /tmp/llmwiki-sync.log 2>&1 &) ; exit 0\" } ] } ]"
