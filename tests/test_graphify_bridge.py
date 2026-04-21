"""Tests for llmwiki.graphify_bridge — Graphify integration."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from llmwiki.graphify_bridge import is_available, GRAPHIFY_OUT


# ─── availability check ─────────────────────────────────────────────


def test_is_available_returns_bool():
    result = is_available()
    assert isinstance(result, bool)


def test_is_available_true_when_graphify_installed():
    """graphifyy is installed in our dev environment."""
    assert is_available() is True


def test_is_available_false_when_not_installed():
    with patch.dict("sys.modules", {"graphify": None}):
        # Force ImportError by removing the module
        import importlib
        from llmwiki import graphify_bridge
        importlib.reload(graphify_bridge)
        # The function does a fresh import each time so we need to mock it
        with patch("builtins.__import__", side_effect=ImportError("no graphify")):
            assert graphify_bridge.is_available() is False
        importlib.reload(graphify_bridge)


# ─── bridge module imports ───────────────────────────────────────────


def test_bridge_module_imports():
    from llmwiki.graphify_bridge import (
        is_available,
        build_graphify_graph,
        export_obsidian,
        export_wiki,
        query_graph,
    )
    assert callable(build_graphify_graph)
    assert callable(export_obsidian)
    assert callable(export_wiki)
    assert callable(query_graph)


# ─── CLI integration ─────────────────────────────────────────────────


def test_cli_graph_has_engine_flag():
    from llmwiki.cli import build_parser

    parser = build_parser()
    # Parse a graph --help to check the engine flag exists
    args = parser.parse_args(["graph", "--engine", "graphify"])
    assert args.engine == "graphify"


def test_cli_graph_engine_default_is_builtin():
    from llmwiki.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["graph"])
    assert args.engine == "builtin"


def test_cli_graph_engine_graphify_accepted():
    from llmwiki.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["graph", "--engine", "graphify"])
    assert args.engine == "graphify"


# ─── pyproject.toml declares graph extra ──────────────────────────────


def test_pyproject_has_graph_extra():
    from llmwiki import REPO_ROOT

    toml_path = REPO_ROOT / "pyproject.toml"
    content = toml_path.read_text(encoding="utf-8")
    assert 'graph = ["graphifyy' in content


# ─── graphify-out in .gitignore ──────────────────────────────────────


def test_gitignore_excludes_graphify_out():
    from llmwiki import REPO_ROOT

    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    assert "graphify-out/" in gitignore


# ─── query_graph returns string ──────────────────────────────────────


def test_query_graph_no_graph_file(tmp_path):
    """When no graph.json exists, return a helpful message."""
    from llmwiki.graphify_bridge import query_graph
    with patch("llmwiki.graphify_bridge.GRAPHIFY_OUT", tmp_path):
        result = query_graph("test question")
    assert "No graph found" in result
