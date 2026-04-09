"""Tests for llmwiki.export_jupyter."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from llmwiki.export_jupyter import (
    export_jupyter,
    _markdown_to_cells,
    _strip_frontmatter,
    _split_lines,
    _build_notebook,
    NBFORMAT,
    NBFORMAT_MINOR,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def wiki_dir(tmp_path: Path) -> Path:
    """Create a minimal wiki directory with test pages."""
    wiki = tmp_path / "wiki"
    for section in ("sources", "entities", "concepts", "syntheses"):
        (wiki / section).mkdir(parents=True)

    # Source page with frontmatter and a code block
    (wiki / "sources" / "session-one.md").write_text(
        '---\ntitle: "Session One"\ntype: source\n---\n\n'
        "# Session One\n\nThis session explored testing.\n\n"
        "```python\ndef hello():\n    return 'world'\n```\n\n"
        "End of session.\n",
        encoding="utf-8",
    )

    # Entity page (no code blocks)
    (wiki / "entities" / "Claude.md").write_text(
        '---\ntitle: "Claude"\ntype: entity\n---\n\n'
        "# Claude\n\nAn AI assistant by Anthropic.\n\n"
        "## Key Facts\n- Built by Anthropic\n",
        encoding="utf-8",
    )

    # Concept page
    (wiki / "concepts" / "RAG.md").write_text(
        "# RAG\n\nRetrieval-Augmented Generation.\n",
        encoding="utf-8",
    )

    # Context file (should be skipped)
    (wiki / "sources" / "_context.md").write_text(
        "Context stub.\n", encoding="utf-8"
    )

    # Empty section (syntheses has no files)
    return wiki


@pytest.fixture()
def output_dir(tmp_path: Path) -> Path:
    return tmp_path / "notebooks"


# ---------------------------------------------------------------------------
# Unit tests: _strip_frontmatter
# ---------------------------------------------------------------------------


class TestStripFrontmatter:
    def test_removes_frontmatter(self) -> None:
        text = '---\ntitle: "Test"\n---\n\n# Body\n'
        assert _strip_frontmatter(text) == "# Body\n"

    def test_no_frontmatter(self) -> None:
        text = "# Just a heading\n"
        assert _strip_frontmatter(text) == text

    def test_incomplete_frontmatter(self) -> None:
        text = "---\ntitle: broken\nno closing\n"
        assert _strip_frontmatter(text) == text


# ---------------------------------------------------------------------------
# Unit tests: _split_lines
# ---------------------------------------------------------------------------


class TestSplitLines:
    def test_empty(self) -> None:
        assert _split_lines("") == []

    def test_single_line(self) -> None:
        assert _split_lines("hello") == ["hello"]

    def test_multi_line(self) -> None:
        result = _split_lines("a\nb\nc")
        assert result == ["a\n", "b\n", "c"]

    def test_trailing_newline(self) -> None:
        result = _split_lines("a\nb\n")
        assert result == ["a\n", "b\n"]


# ---------------------------------------------------------------------------
# Unit tests: _markdown_to_cells
# ---------------------------------------------------------------------------


class TestMarkdownToCells:
    def test_plain_markdown(self) -> None:
        cells = _markdown_to_cells("# Heading\n\nSome text.")
        assert len(cells) == 1
        assert cells[0]["cell_type"] == "markdown"

    def test_code_block_extraction(self) -> None:
        md = "Before.\n\n```python\nprint('hi')\n```\n\nAfter."
        cells = _markdown_to_cells(md)
        assert len(cells) == 3
        assert cells[0]["cell_type"] == "markdown"
        assert cells[1]["cell_type"] == "code"
        assert cells[2]["cell_type"] == "markdown"
        # Code cell should contain the code
        code_src = "".join(cells[1]["source"])
        assert "print('hi')" in code_src

    def test_multiple_code_blocks(self) -> None:
        md = (
            "Intro.\n\n```bash\necho hi\n```\n\n"
            "Middle.\n\n```python\nx = 1\n```\n\nEnd."
        )
        cells = _markdown_to_cells(md)
        code_cells = [c for c in cells if c["cell_type"] == "code"]
        md_cells = [c for c in cells if c["cell_type"] == "markdown"]
        assert len(code_cells) == 2
        assert len(md_cells) == 3

    def test_empty_content(self) -> None:
        cells = _markdown_to_cells("")
        assert len(cells) == 1
        assert cells[0]["cell_type"] == "markdown"


# ---------------------------------------------------------------------------
# Unit tests: _build_notebook
# ---------------------------------------------------------------------------


class TestBuildNotebook:
    def test_notebook_structure(self) -> None:
        nb = _build_notebook("Test", [("page1", "# Page 1\nContent.")])
        assert nb["nbformat"] == NBFORMAT
        assert nb["nbformat_minor"] == NBFORMAT_MINOR
        assert "kernelspec" in nb["metadata"]
        assert len(nb["cells"]) >= 2  # title cell + at least one page

    def test_empty_pages(self) -> None:
        nb = _build_notebook("Empty", [])
        assert len(nb["cells"]) == 1  # just the title cell


# ---------------------------------------------------------------------------
# Integration tests: export_jupyter
# ---------------------------------------------------------------------------


class TestExportJupyter:
    def test_creates_notebooks(
        self, wiki_dir: Path, output_dir: Path
    ) -> None:
        created = export_jupyter(wiki_dir, output_dir)
        assert output_dir.exists()
        # Should create notebooks for sources, entities, concepts (not syntheses — empty)
        names = {p.name for p in created}
        assert "sources.ipynb" in names
        assert "entities.ipynb" in names
        assert "concepts.ipynb" in names
        assert "syntheses.ipynb" not in names  # empty section skipped

    def test_valid_ipynb(self, wiki_dir: Path, output_dir: Path) -> None:
        export_jupyter(wiki_dir, output_dir)
        for nb_path in output_dir.glob("*.ipynb"):
            data = json.loads(nb_path.read_text(encoding="utf-8"))
            assert data["nbformat"] == 4
            assert "cells" in data
            for cell in data["cells"]:
                assert cell["cell_type"] in ("markdown", "code")
                assert isinstance(cell["source"], list)

    def test_skips_context_files(
        self, wiki_dir: Path, output_dir: Path
    ) -> None:
        export_jupyter(wiki_dir, output_dir)
        sources_nb = json.loads(
            (output_dir / "sources.ipynb").read_text(encoding="utf-8")
        )
        all_text = " ".join(
            "".join(c["source"]) for c in sources_nb["cells"]
        )
        assert "Context stub" not in all_text

    def test_strips_frontmatter(
        self, wiki_dir: Path, output_dir: Path
    ) -> None:
        export_jupyter(wiki_dir, output_dir)
        entities_nb = json.loads(
            (output_dir / "entities.ipynb").read_text(encoding="utf-8")
        )
        all_text = " ".join(
            "".join(c["source"]) for c in entities_nb["cells"]
        )
        assert "type: entity" not in all_text
        assert "Claude" in all_text

    def test_code_blocks_become_code_cells(
        self, wiki_dir: Path, output_dir: Path
    ) -> None:
        export_jupyter(wiki_dir, output_dir)
        sources_nb = json.loads(
            (output_dir / "sources.ipynb").read_text(encoding="utf-8")
        )
        code_cells = [
            c for c in sources_nb["cells"] if c["cell_type"] == "code"
        ]
        assert len(code_cells) >= 1
        code_text = "".join(code_cells[0]["source"])
        assert "hello" in code_text

    def test_nonexistent_wiki_dir(self, tmp_path: Path) -> None:
        result = export_jupyter(tmp_path / "nope", tmp_path / "out")
        assert result == []

    def test_string_paths(self, wiki_dir: Path, output_dir: Path) -> None:
        """Accepts string paths, not just Path objects."""
        created = export_jupyter(str(wiki_dir), str(output_dir))
        assert len(created) > 0
