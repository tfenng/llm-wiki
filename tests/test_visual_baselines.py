"""Tests for the visual-baseline framework (v1.2.0 · #113)."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import pytest

from llmwiki import REPO_ROOT
from llmwiki.visual_baselines import (
    DEFAULT_BASELINES_FILENAME,
    compare_against_baselines,
    format_comparison,
    generate_baselines,
    hash_png,
    is_clean,
    load_baselines,
    save_baselines,
)


# ─── Test helpers ─────────────────────────────────────────────────────


def _write_png(path: Path, body: bytes = b"dummy-png-data") -> Path:
    """Write a fake PNG file. We don't actually encode PNG — the module
    treats files as opaque bytes, so any content works."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(body)
    return path


def _sha(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


# ─── hash_png ─────────────────────────────────────────────────────────


def test_hash_png_matches_sha256(tmp_path: Path):
    body = b"pretend this is a PNG"
    path = _write_png(tmp_path / "x.png", body)
    assert hash_png(path) == _sha(body)


def test_hash_png_raises_on_missing(tmp_path: Path):
    with pytest.raises(FileNotFoundError, match="does not exist"):
        hash_png(tmp_path / "nope.png")


def test_hash_png_handles_large_file(tmp_path: Path):
    # 1 MiB — forces multiple 64 KiB read chunks to hit.
    body = os.urandom(1024 * 1024)
    path = _write_png(tmp_path / "big.png", body)
    assert hash_png(path) == _sha(body)


def test_hash_png_deterministic_across_calls(tmp_path: Path):
    path = _write_png(tmp_path / "x.png", b"same content")
    assert hash_png(path) == hash_png(path)


# ─── load_baselines / save_baselines ──────────────────────────────────


def test_load_baselines_missing_returns_empty(tmp_path: Path):
    assert load_baselines(tmp_path / "none.json") == {}


def test_load_baselines_unreadable_json_returns_empty(tmp_path: Path):
    p = tmp_path / "bad.json"
    p.write_text("not json at all", encoding="utf-8")
    assert load_baselines(p) == {}


def test_load_accepts_legacy_string_shape(tmp_path: Path):
    p = tmp_path / "legacy.json"
    p.write_text(json.dumps({"home.png": "abc123"}), encoding="utf-8")
    baselines = load_baselines(p)
    assert baselines == {"home.png": {"sha256": "abc123", "size": 0}}


def test_load_accepts_full_entry_shape(tmp_path: Path):
    p = tmp_path / "full.json"
    p.write_text(
        json.dumps({"x.png": {"sha256": "def", "size": 42}}),
        encoding="utf-8",
    )
    assert load_baselines(p) == {"x.png": {"sha256": "def", "size": 42}}


def test_save_roundtrip(tmp_path: Path):
    original = {"a.png": {"sha256": "1", "size": 10}}
    out = tmp_path / "sub" / "b.json"
    save_baselines(original, out)
    assert load_baselines(out) == original


def test_save_writes_sorted_indented_json(tmp_path: Path):
    out = tmp_path / "b.json"
    save_baselines(
        {"b.png": {"sha256": "2", "size": 2}, "a.png": {"sha256": "1", "size": 1}},
        out,
    )
    text = out.read_text(encoding="utf-8")
    # sorted: a.png appears before b.png
    assert text.index("a.png") < text.index("b.png")
    # indent=2 is diff-friendly
    assert "  " in text


def test_save_creates_parent_dirs(tmp_path: Path):
    out = tmp_path / "nested" / "dir" / "b.json"
    save_baselines({"a.png": {"sha256": "x", "size": 0}}, out)
    assert out.is_file()


# ─── generate_baselines ──────────────────────────────────────────────


def test_generate_hashes_every_png(tmp_path: Path):
    a = _write_png(tmp_path / "a.png", b"aaa")
    b = _write_png(tmp_path / "b.png", b"bbb")
    out = generate_baselines(tmp_path)
    assert set(out.keys()) == {"a.png", "b.png"}
    assert out["a.png"]["sha256"] == _sha(b"aaa")
    assert out["b.png"]["sha256"] == _sha(b"bbb")


def test_generate_includes_file_size(tmp_path: Path):
    _write_png(tmp_path / "x.png", b"123456")
    out = generate_baselines(tmp_path)
    assert out["x.png"]["size"] == 6


def test_generate_uses_relative_paths(tmp_path: Path):
    # A screenshot inside a subdir should key by its relative path, not
    # absolute — otherwise the baseline file isn't portable.
    _write_png(tmp_path / "sub" / "dir" / "deep.png", b"xyz")
    out = generate_baselines(tmp_path)
    assert "sub/dir/deep.png" in out


def test_generate_ignores_non_png(tmp_path: Path):
    _write_png(tmp_path / "real.png")
    (tmp_path / "notes.md").write_text("not a screenshot", encoding="utf-8")
    (tmp_path / "data.json").write_text("{}", encoding="utf-8")
    out = generate_baselines(tmp_path)
    assert set(out.keys()) == {"real.png"}


def test_generate_missing_dir_returns_empty(tmp_path: Path):
    assert generate_baselines(tmp_path / "nope") == {}


def test_generate_writes_to_baselines_path_when_provided(tmp_path: Path):
    _write_png(tmp_path / "a.png", b"aa")
    out = tmp_path / "baselines.json"
    generate_baselines(tmp_path, baselines_path=out)
    assert out.is_file()
    loaded = load_baselines(out)
    assert "a.png" in loaded


def test_generate_is_deterministic(tmp_path: Path):
    _write_png(tmp_path / "a.png", b"aa")
    _write_png(tmp_path / "b.png", b"bb")
    out1 = generate_baselines(tmp_path)
    out2 = generate_baselines(tmp_path)
    assert out1 == out2


# ─── compare_against_baselines ────────────────────────────────────────


def _seed_baselines(tmp_path: Path) -> tuple[Path, Path]:
    """Helper: produce a screenshots dir + a committed baseline that
    matches. Returns ``(screenshots_dir, baselines_path)``."""
    shots = tmp_path / "shots"
    shots.mkdir()
    _write_png(shots / "home.png", b"home-v1")
    _write_png(shots / "session.png", b"session-v1")
    manifest = tmp_path / "baselines.json"
    generate_baselines(shots, baselines_path=manifest)
    return shots, manifest


def test_compare_all_match(tmp_path: Path):
    shots, manifest = _seed_baselines(tmp_path)
    result = compare_against_baselines(shots, manifest)
    assert set(result["match"]) == {"home.png", "session.png"}
    assert result["drift"] == []
    assert result["new"] == []
    assert result["missing"] == []


def test_compare_detects_drift(tmp_path: Path):
    shots, manifest = _seed_baselines(tmp_path)
    # Mutate one screenshot
    _write_png(shots / "home.png", b"home-changed")
    result = compare_against_baselines(shots, manifest)
    assert result["drift"] == ["home.png"]
    assert "session.png" in result["match"]


def test_compare_detects_new_screenshots(tmp_path: Path):
    shots, manifest = _seed_baselines(tmp_path)
    _write_png(shots / "new-surface.png", b"new!")
    result = compare_against_baselines(shots, manifest)
    assert result["new"] == ["new-surface.png"]
    assert len(result["match"]) == 2


def test_compare_detects_missing_screenshots(tmp_path: Path):
    shots, manifest = _seed_baselines(tmp_path)
    # Remove one of the screenshots the baseline knows about
    (shots / "session.png").unlink()
    result = compare_against_baselines(shots, manifest)
    assert result["missing"] == ["session.png"]
    assert "home.png" in result["match"]


def test_compare_all_buckets_populated(tmp_path: Path):
    shots, manifest = _seed_baselines(tmp_path)
    _write_png(shots / "home.png", b"changed")       # drift
    _write_png(shots / "added.png", b"new")          # new
    (shots / "session.png").unlink()                 # missing
    result = compare_against_baselines(shots, manifest)
    assert result["drift"] == ["home.png"]
    assert result["new"] == ["added.png"]
    assert result["missing"] == ["session.png"]


def test_compare_results_are_sorted(tmp_path: Path):
    shots = tmp_path / "s"
    shots.mkdir()
    _write_png(shots / "z.png", b"z")
    _write_png(shots / "a.png", b"a")
    _write_png(shots / "m.png", b"m")
    manifest = tmp_path / "b.json"
    generate_baselines(shots, baselines_path=manifest)

    # Mutate to push all three into drift
    _write_png(shots / "z.png", b"zz")
    _write_png(shots / "a.png", b"aa")
    _write_png(shots / "m.png", b"mm")

    result = compare_against_baselines(shots, manifest)
    assert result["drift"] == ["a.png", "m.png", "z.png"]


# ─── format_comparison ────────────────────────────────────────────────


def test_format_comparison_clean_result():
    result = {"match": ["a.png", "b.png"], "drift": [], "new": [], "missing": []}
    out = format_comparison(result)
    assert "2 match" in out
    assert "0 drift" in out


def test_format_comparison_highlights_drift():
    result = {"match": [], "drift": ["home.png"], "new": [], "missing": []}
    out = format_comparison(result)
    assert "Drifted:" in out
    assert "home.png" in out


def test_format_comparison_mentions_new_hint():
    result = {"match": [], "drift": [], "new": ["added.png"], "missing": []}
    out = format_comparison(result)
    assert "regenerate after review" in out


def test_format_comparison_missing_hint():
    result = {"match": [], "drift": [], "new": [], "missing": ["gone.png"]}
    out = format_comparison(result)
    assert "removed surface" in out or "prune" in out


# ─── is_clean ─────────────────────────────────────────────────────────


def test_is_clean_true_when_everything_matches():
    result = {"match": ["a.png"], "drift": [], "new": [], "missing": []}
    assert is_clean(result)


def test_is_clean_false_with_drift():
    assert not is_clean({"match": [], "drift": ["x"], "new": [], "missing": []})


def test_is_clean_false_with_new():
    assert not is_clean({"match": [], "drift": [], "new": ["x"], "missing": []})


def test_is_clean_false_with_missing():
    assert not is_clean({"match": [], "drift": [], "new": [], "missing": ["x"]})


# ─── Repo-level guardrails ────────────────────────────────────────────


def test_default_baselines_filename_is_stable():
    # Don't let someone quietly rename this — the workflow scripts +
    # docs all reference `baselines.json` explicitly.
    assert DEFAULT_BASELINES_FILENAME == "baselines.json"


def test_baselines_readme_exists():
    path = REPO_ROOT / "tests" / "e2e" / "visual_baselines" / "README.md"
    assert path.is_file(), (
        "tests/e2e/visual_baselines/README.md missing — it points "
        "reviewers at docs/testing/visual-regression.md"
    )


def test_update_script_is_executable():
    script = REPO_ROOT / "scripts" / "update-visual-baselines.sh"
    assert script.is_file()
    assert os.access(script, os.X_OK), (
        "scripts/update-visual-baselines.sh must be executable; "
        "run `chmod +x` on it"
    )


def test_docs_visual_regression_exists():
    doc = REPO_ROOT / "docs" / "testing" / "visual-regression.md"
    assert doc.is_file()
    text = doc.read_text(encoding="utf-8")
    # Doc must cover the workflow + the CLI summary format
    for keyword in ("baselines.json", "drift", "missing", "update-visual-baselines"):
        assert keyword in text
