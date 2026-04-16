"""Tests for flat raw/ naming scheme (v1.0, #141)."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from llmwiki.convert import flat_output_name


def test_basic_flat_name():
    started = datetime(2026, 4, 16, 10, 30, tzinfo=timezone.utc)
    result = flat_output_name(started, "ai-newsletter", "kind-tinkering-hejlsberg")
    assert result == "2026-04-16T10-30-ai-newsletter-kind-tinkering-hejlsberg.md"


def test_midnight():
    started = datetime(2026, 1, 1, 0, 0, tzinfo=timezone.utc)
    result = flat_output_name(started, "demo", "test")
    assert result == "2026-01-01T00-00-demo-test.md"


def test_single_digit_hour():
    started = datetime(2026, 3, 5, 9, 5, tzinfo=timezone.utc)
    result = flat_output_name(started, "myproject", "slug")
    assert result == "2026-03-05T09-05-myproject-slug.md"


def test_ends_with_md():
    result = flat_output_name(
        datetime(2026, 4, 1, 14, 0, tzinfo=timezone.utc),
        "proj",
        "test-slug",
    )
    assert result.endswith(".md")


def test_no_slashes_in_name():
    """Flat naming must not produce nested directories."""
    result = flat_output_name(
        datetime(2026, 4, 1, 14, 0, tzinfo=timezone.utc),
        "my-project",
        "my-slug",
    )
    assert "/" not in result
    assert "\\" not in result


def test_chronological_sort():
    """Files should sort chronologically by name."""
    names = [
        flat_output_name(datetime(2026, 4, 16, 10, 0, tzinfo=timezone.utc), "a", "s1"),
        flat_output_name(datetime(2026, 4, 16, 9, 0, tzinfo=timezone.utc), "a", "s2"),
        flat_output_name(datetime(2026, 4, 15, 23, 59, tzinfo=timezone.utc), "b", "s3"),
    ]
    assert sorted(names) == [names[2], names[1], names[0]]  # oldest first


def test_project_embedded():
    """Project slug is in the filename for traceability."""
    result = flat_output_name(
        datetime(2026, 4, 1, 14, 0, tzinfo=timezone.utc),
        "germanly",
        "slug",
    )
    assert "germanly" in result


def test_subagent_slug():
    """Subagent slugs (with -subagent- suffix) work fine."""
    result = flat_output_name(
        datetime(2026, 4, 1, 14, 0, tzinfo=timezone.utc),
        "research",
        "my-slug-subagent-abc12345",
    )
    assert "subagent" in result
    assert "/" not in result
