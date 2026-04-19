# Visual-regression baselines

> Status: shipped in v1.2.0 (#113). Captures pixel-identical baselines
> of approved UI surfaces and flags drift in CI. Stdlib-only — no
> Pillow / image-diff libraries.

## Why hashing, not perceptual diff

llmwiki's "approved UI surfaces" render from deterministic CSS + fixed
demo data. Given the same Playwright browser + same viewport, the PNG
bytes are identical. A hash change means something *did* change.

Pillow or pixelmatch would add a runtime dependency. The project rule
is stdlib-only. Hash-compare is harsher (no tolerance for antialiasing
drift), but the upside is visible: every pixel difference demands an
explicit baseline update, which forces a review of the change.

## Surfaces currently tracked

The baselines file (`tests/e2e/visual_baselines/baselines.json`) holds
one entry per screenshot produced by the E2E suite. Today's set:

- **Home page** × 4 breakpoints × 2 themes (8)
- **Session page** × 4 breakpoints × 2 themes (8)
- **Prototype hub** (from #114) — 6 states (shipped in site/prototypes/,
  reachable in the E2E suite as standalone pages)

Any file under `tests/e2e/screenshots/` with a `.png` extension is
included automatically — add new surfaces by adding a Cucumber scenario
that captures them.

## Workflow

### First run — generate baselines

```bash
# 1. Run the E2E suite to produce screenshots
pytest tests/e2e/test_visual_regression.py

# 2. Freeze them as the new baselines
scripts/update-visual-baselines.sh

# 3. Commit
git add tests/e2e/visual_baselines/baselines.json
git commit -S -m "test: seed visual baselines"
```

### On every PR — CI compares

The regression test loads `tests/e2e/visual_baselines/baselines.json`,
hashes every PNG under `tests/e2e/screenshots/`, and produces a
four-bucket comparison:

| Bucket | Meaning | Test verdict |
|---|---|---|
| `match` | live hash == baseline hash | passes |
| `drift` | live hash != baseline hash | **fails** — review + refresh |
| `new` | screenshot captured with no baseline | **fails** — run update script |
| `missing` | baseline present, screenshot gone | **fails** — prune or restore |

The CLI summary looks like:

```
✓ 22 match
✗ 1 drift
+ 0 new
- 0 missing

Drifted:
  • home-desktop-dark.png
```

### When drift is intentional — refresh

1. Visually inspect the drifted file(s). Browser-based image-diff
   tools work well (e.g., GitHub's built-in image comparer on the PR).
2. If the change is the desired effect of your PR, regenerate:
   ```bash
   scripts/update-visual-baselines.sh
   git add tests/e2e/visual_baselines/baselines.json
   git commit -S -m "test: refresh visual baselines — light-mode palette bump"
   ```
3. If the change is unintentional, fix the offending CSS before
   regenerating.

## Python API

```python
from pathlib import Path
from llmwiki.visual_baselines import (
    generate_baselines,
    compare_against_baselines,
    format_comparison,
    is_clean,
)

# Regenerate (first-time or after reviewing drift)
generate_baselines(
    Path("tests/e2e/screenshots"),
    baselines_path=Path("tests/e2e/visual_baselines/baselines.json"),
)

# Check — returns a dict with match/drift/new/missing lists
result = compare_against_baselines(
    Path("tests/e2e/screenshots"),
    Path("tests/e2e/visual_baselines/baselines.json"),
)
print(format_comparison(result))
if not is_clean(result):
    raise SystemExit(1)
```

## CI wiring

The GitHub Actions `e2e.yml` workflow runs Playwright + pytest-bdd,
producing the screenshots under `tests/e2e/screenshots/`. A follow-up
step in the same workflow calls `compare_against_baselines` and fails
the job if anything drifts. Artifacts (both the drifted PNGs and the
baseline JSON) are uploaded on failure so reviewers can download and
diff without rerunning.

## Non-goals

- **Cross-browser baselines.** We compare against Chromium-produced
  PNGs only. Firefox / WebKit render at sub-pixel differences that
  don't survive byte-hash comparison; pixel-diff libraries could
  handle this, but add a runtime dep we've declined.
- **Responsive drift detection across every viewport.** Today we pin
  four breakpoints (phone 375, tablet 768, laptop 1280, desktop 1920).
  Fluid-resize bugs that only appear between those widths can slip
  past.
- **Animation frame capture.** Screenshots are captured once per
  scenario after the page settles. Hover / transition states are out
  of scope.

## Related

- `llmwiki/visual_baselines.py` — the hashing library
- `scripts/update-visual-baselines.sh` — driver
- `tests/e2e/test_visual_regression.py` — the E2E screenshot capture
- `tests/e2e/visual_baselines/baselines.json` — committed manifest
- `#113` — this issue
- `#114` — the prototype hub whose states we regression-test
