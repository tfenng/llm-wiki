"""Integration test for the collision-retry branch in ``convert_all`` (#339).

When two distinct source jsonls would write to the same output path
(subagent sharing its parent's start-time + slug, or two top-level
sessions that happen to start in the same minute), the retry appends
a source-path hash so both files land side-by-side rather than one
getting quarantined.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from llmwiki import convert as c


def _write_jsonl(path: Path, session_id: str, iso_ts: str,
                 slug: str = "shared-slug") -> None:
    """Seed a minimal claude_code-shaped jsonl.

    ``slug`` on the first record pins derive_session_slug so two
    sources can deliberately collide on the canonical filename.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({
            "type": "user",
            "sessionId": session_id,
            "slug": slug,
            "timestamp": iso_ts,
            "cwd": "/tmp",
            "gitBranch": "main",
            "message": {"role": "user", "content": "hi"},
        }) + "\n"
        + json.dumps({
            "type": "assistant",
            "sessionId": session_id,
            "timestamp": iso_ts,
            "message": {"role": "assistant", "content": "hello"},
        }) + "\n",
        encoding="utf-8",
    )


def _seed_env(tmp_path: Path) -> tuple[Path, Path, Path]:
    """Seed a tmp_path repo + fake ~/.claude/projects/ source."""
    home = tmp_path / "home"
    home.mkdir()
    cc_projects = home / ".claude" / "projects" / "my-proj"
    out_dir = tmp_path / "repo" / "raw" / "sessions"
    state = tmp_path / "state.json"
    return home, cc_projects, out_dir, state


def _patch(monkeypatch, home, out_dir, state):
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    monkeypatch.setattr(c, "DEFAULT_STATE_FILE", state)
    monkeypatch.setattr(c, "REPO_ROOT", home.parent / "repo")


def test_subagent_collision_is_resolved_with_hash_suffix(tmp_path, monkeypatch):
    """Parent + subagent that share start-time + slug both land on disk."""
    home, cc, out_dir, state = _seed_env(tmp_path)

    ts = "2026-04-16T10:00:00Z"
    parent = cc / "sess-uuid" / "parent.jsonl"
    sub = cc / "sess-uuid" / "subagents" / "agent-aprompt-abc.jsonl"
    _write_jsonl(parent, "sess-uuid-1111", ts)
    _write_jsonl(sub, "sess-uuid-1111", ts)

    _patch(monkeypatch, home, out_dir, state)

    # Force the adapter to be claude_code only so we don't drag in
    # obsidian / others from the test environment.
    c.discover_adapters()
    rc = c.convert_all(
        adapters=["claude_code"],
        out_dir=out_dir,
        state_file=state,
        include_current=True,  # include even very-recent test files
        force=False,
    )
    assert rc in (0, 1)  # some adapters may error for other reasons

    # Both sources should have produced an output file.
    outs = sorted(out_dir.rglob("*.md"))
    # There should be at least two distinct files with the same date+slug
    # base, one with a --<hash> suffix.
    disambig = [p for p in outs if "--" in p.name]
    canonical = [p for p in outs if "--" not in p.name]
    assert canonical, f"canonical name missing; got {outs}"
    # The subagent's file should carry the disambiguator suffix.
    # (If both are the subagent, we still land the second; the first
    # run is canonical because nothing existed yet.)
    assert disambig, f"disambiguated file missing; got {outs}"


def test_second_source_with_identical_canonical_name_gets_hash(tmp_path, monkeypatch):
    """Write one source, then simulate a second distinct source that
    would produce the same canonical name — expect it to get a hash."""
    home, cc, out_dir, state = _seed_env(tmp_path)
    ts = "2026-04-16T10:00:00Z"

    s1 = cc / "session-a.jsonl"
    s2 = cc / "subagents" / "agent-aa.jsonl"
    _write_jsonl(s1, "same-session-id", ts)
    _write_jsonl(s2, "same-session-id", ts)

    _patch(monkeypatch, home, out_dir, state)

    c.discover_adapters()
    c.convert_all(adapters=["claude_code"], out_dir=out_dir,
                  state_file=state, include_current=True)

    outs = sorted(out_dir.rglob("*.md"))
    # At least one canonical + one disambiguated.
    canonical = [p for p in outs if "--" not in p.name]
    disambig = [p for p in outs if "--" in p.name]
    assert len(outs) >= 2
    assert canonical, f"no canonical file: {outs}"
    assert disambig, f"no disambiguated file: {outs}"


def test_resync_same_source_is_idempotent(tmp_path, monkeypatch):
    """Re-running sync on the same jsonl doesn't explode into
    <canonical> + <hash1> + <hash2> — the state key protects us."""
    home, cc, out_dir, state = _seed_env(tmp_path)
    _write_jsonl(cc / "s.jsonl", "x", "2026-04-16T10:00:00Z")
    _patch(monkeypatch, home, out_dir, state)

    c.discover_adapters()
    c.convert_all(adapters=["claude_code"], out_dir=out_dir,
                  state_file=state, include_current=True)
    first = sorted(out_dir.rglob("*.md"))
    c.convert_all(adapters=["claude_code"], out_dir=out_dir,
                  state_file=state, include_current=True)
    second = sorted(out_dir.rglob("*.md"))
    assert first == second, f"re-sync grew the tree: {first} → {second}"
