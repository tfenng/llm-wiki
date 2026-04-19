#!/usr/bin/env bash
# Regenerate tests/e2e/visual_baselines/baselines.json (#113).
#
# Usage:
#   scripts/update-visual-baselines.sh                    # default screenshots dir
#   scripts/update-visual-baselines.sh tests/e2e/screenshots   # custom
#
# Prerequisite: screenshots already exist at the target directory. The
# E2E suite's `visual_regression` scenarios produce them — run:
#   pytest tests/e2e/test_visual_regression.py
# before this script.

set -euo pipefail

cd "$(dirname "$0")/.."

screenshots_dir="${1:-tests/e2e/screenshots}"
baselines_path="${2:-tests/e2e/visual_baselines/baselines.json}"

if [ ! -d "$screenshots_dir" ]; then
  echo "error: screenshots directory not found: $screenshots_dir" >&2
  echo "hint: run pytest tests/e2e/ first to generate them" >&2
  exit 1
fi

png_count="$(find "$screenshots_dir" -name '*.png' | wc -l | tr -d ' ')"
if [ "$png_count" -eq 0 ]; then
  echo "error: no PNGs under $screenshots_dir" >&2
  exit 1
fi

echo "→ Hashing $png_count screenshot(s) under $screenshots_dir …"

python3 -c "
from pathlib import Path
from llmwiki.visual_baselines import generate_baselines

count = len(generate_baselines(
    Path('$screenshots_dir'),
    baselines_path=Path('$baselines_path'),
))
print(f'  wrote {count} baseline entries → $baselines_path')
"

echo ""
echo "✓ Review the diff, then:"
echo "    git add $baselines_path"
echo "    git commit -S -m 'test: refresh visual baselines'"
