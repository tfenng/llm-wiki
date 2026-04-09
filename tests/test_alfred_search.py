"""Tests for integrations/alfred/search.py."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# Add the Alfred integration to the path
ALFRED_DIR = Path(__file__).resolve().parent.parent / "integrations" / "alfred"
sys.path.insert(0, str(ALFRED_DIR))

import search  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def project_with_index(tmp_path: Path) -> Path:
    """Create a project with a search-index.json."""
    site = tmp_path / "site"
    site.mkdir()
    index = [
        {"title": "Session One", "url": "sources/session-one.html", "body": "Testing framework setup"},
        {"title": "Claude", "url": "entities/Claude.html", "body": "AI assistant by Anthropic"},
        {"title": "RAG", "url": "concepts/RAG.html", "body": "Retrieval-Augmented Generation"},
    ]
    (site / "search-index.json").write_text(json.dumps(index), encoding="utf-8")
    return tmp_path


@pytest.fixture()
def project_with_wiki(tmp_path: Path) -> Path:
    """Create a project with wiki/ markdown files but no search index."""
    wiki = tmp_path / "wiki"
    (wiki / "sources").mkdir(parents=True)
    (wiki / "entities").mkdir(parents=True)
    (wiki / "sources" / "session-one.md").write_text(
        "# Session One\n\nTesting framework.\n", encoding="utf-8"
    )
    (wiki / "entities" / "Claude.md").write_text(
        "# Claude\n\nAI assistant.\n", encoding="utf-8"
    )
    (wiki / "sources" / "_context.md").write_text("Context.\n", encoding="utf-8")
    return tmp_path


# ---------------------------------------------------------------------------
# Tests: load_search_index
# ---------------------------------------------------------------------------


class TestLoadSearchIndex:
    def test_loads_valid_index(self, project_with_index: Path) -> None:
        result = search.load_search_index(project_with_index)
        assert result is not None
        assert len(result) == 3

    def test_returns_none_when_missing(self, tmp_path: Path) -> None:
        assert search.load_search_index(tmp_path) is None

    def test_returns_none_on_invalid_json(self, tmp_path: Path) -> None:
        site = tmp_path / "site"
        site.mkdir()
        (site / "search-index.json").write_text("not json", encoding="utf-8")
        assert search.load_search_index(tmp_path) is None


# ---------------------------------------------------------------------------
# Tests: scan_wiki_titles
# ---------------------------------------------------------------------------


class TestScanWikiTitles:
    def test_finds_pages(self, project_with_wiki: Path) -> None:
        results = search.scan_wiki_titles(project_with_wiki)
        titles = {r["title"] for r in results}
        assert "Session One" in titles
        assert "Claude" in titles

    def test_skips_context_files(self, project_with_wiki: Path) -> None:
        results = search.scan_wiki_titles(project_with_wiki)
        paths = {r["path"] for r in results}
        assert not any("_context" in p for p in paths)

    def test_empty_dir(self, tmp_path: Path) -> None:
        assert search.scan_wiki_titles(tmp_path) == []


# ---------------------------------------------------------------------------
# Tests: search
# ---------------------------------------------------------------------------


class TestSearch:
    def test_title_match(self) -> None:
        entries = [
            {"title": "Claude", "body": "assistant", "path": "x.html"},
            {"title": "Other", "body": "something", "path": "y.html"},
        ]
        results = search.search("Claude", entries)
        assert len(results) == 1
        assert results[0]["title"] == "Claude"

    def test_body_match(self) -> None:
        entries = [
            {"title": "Page", "body": "retrieval augmented generation", "path": "x.html"},
        ]
        results = search.search("retrieval", entries)
        assert len(results) == 1

    def test_empty_query_returns_all(self) -> None:
        entries = [{"title": f"P{i}", "path": f"{i}.html"} for i in range(5)]
        results = search.search("", entries)
        assert len(results) == 5

    def test_no_match(self) -> None:
        entries = [{"title": "X", "body": "Y", "path": "z.html"}]
        assert search.search("notfound", entries) == []


# ---------------------------------------------------------------------------
# Tests: to_alfred_json
# ---------------------------------------------------------------------------


class TestToAlfredJson:
    def test_produces_items(self) -> None:
        matches = [{"title": "Claude", "path": "entities/Claude.html", "section": "Entities"}]
        result = search.to_alfred_json(matches)
        assert "items" in result
        assert len(result["items"]) == 1
        assert result["items"][0]["title"] == "Claude"
        assert "localhost:8765" in result["items"][0]["arg"]

    def test_empty_results_show_message(self) -> None:
        result = search.to_alfred_json([])
        assert len(result["items"]) == 1
        assert result["items"][0]["title"] == "No results found"
        assert result["items"][0].get("valid") is False
