"""Tests for the canonical frontmatter parser (#273)."""

from __future__ import annotations

import pytest

from llmwiki._frontmatter import (
    parse_frontmatter,
    parse_frontmatter_dict,
    parse_frontmatter_or_none,
    _parse_scalar,
)


# ─── parse_frontmatter: happy paths ──────────────────────────────────


def test_parses_basic_frontmatter():
    text = '---\ntitle: "Example"\ntype: entity\n---\n\nBody.\n'
    meta, body = parse_frontmatter(text)
    assert meta["title"] == "Example"
    assert meta["type"] == "entity"
    assert body.startswith("\nBody.")


def test_handles_missing_frontmatter():
    text = "# Just body\n\nContent\n"
    meta, body = parse_frontmatter(text)
    assert meta == {}
    assert body == text


def test_empty_frontmatter_block():
    text = "---\n---\nbody\n"
    meta, body = parse_frontmatter(text)
    assert meta == {}
    assert body == "body\n"


def test_ignores_malformed_lines():
    text = "---\ntitle: X\nnot a key line\nvalid: 1\n---\n"
    meta, _ = parse_frontmatter(text)
    assert meta["title"] == "X"
    assert meta["valid"] == 1
    assert "not a key line" not in meta


# ─── _parse_scalar edge cases ────────────────────────────────────────


@pytest.mark.parametrize("raw,expected", [
    ("123", 123),
    ("-17", -17),
    ("0", 0),
    ("3.14", 3.14),
    ("true", True),
    ("True", True),
    ("yes", True),
    ("false", False),
    ("no", False),
    ("", ""),
    ('"quoted"', "quoted"),
    ("'single'", "single"),
    ("plain string", "plain string"),
    ("[]", []),
    ("[a, b, c]", ["a", "b", "c"]),
    ('["x", "y"]', ["x", "y"]),
    ("[1, 2, 3]", [1, 2, 3]),
])
def test_parse_scalar_variants(raw, expected):
    assert _parse_scalar(raw) == expected


def test_parse_scalar_whitespace_agnostic():
    assert _parse_scalar("  123  ") == 123


# ─── legacy signature wrappers ───────────────────────────────────────


def test_parse_frontmatter_dict_returns_meta_only():
    text = '---\ntitle: X\n---\nbody\n'
    assert parse_frontmatter_dict(text) == {"title": "X"}


def test_parse_frontmatter_or_none_returns_raw_text():
    text = '---\ntitle: "Ex"\ntags: [a, b]\n---\nbody\n'
    fm, body = parse_frontmatter_or_none(text)
    assert fm is not None
    assert 'title: "Ex"' in fm
    assert 'tags: [a, b]' in fm
    assert body == "body\n"


def test_parse_frontmatter_or_none_missing():
    fm, body = parse_frontmatter_or_none("no frontmatter\n")
    assert fm is None
    assert body == "no frontmatter\n"


# ─── Inline list is properly parsed ──────────────────────────────────


def test_inline_list_returns_python_list():
    text = '---\ntags: [claude-code, session-transcript]\n---\n'
    meta, _ = parse_frontmatter(text)
    assert meta["tags"] == ["claude-code", "session-transcript"]


def test_quoted_list_elements_stripped():
    text = '---\ntags: ["a b", "c d"]\n---\n'
    meta, _ = parse_frontmatter(text)
    assert meta["tags"] == ["a b", "c d"]


def test_int_and_bool_scalars_typed():
    text = '---\ncount: 42\nenabled: true\ntitle: X\n---\n'
    meta, _ = parse_frontmatter(text)
    assert meta["count"] == 42
    assert meta["enabled"] is True
    assert meta["title"] == "X"


def test_round_trip_simple_case():
    """Write a page, read it back, frontmatter round-trips."""
    text = '---\ntitle: "Round trip"\ntype: source\n---\n\n# Body\n'
    meta, body = parse_frontmatter(text)
    assert meta == {"title": "Round trip", "type": "source"}
    assert body.strip() == "# Body"
