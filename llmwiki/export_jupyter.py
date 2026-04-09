"""Jupyter notebook export for llmwiki (stdlib only).

Converts wiki pages into .ipynb notebooks — one notebook per wiki section
(sources, entities, concepts, syntheses). Markdown content becomes markdown
cells; fenced code blocks become code cells.

Usage:
    from llmwiki.export_jupyter import export_jupyter
    export_jupyter(Path("wiki"), Path("/tmp/wiki-notebooks"))

Output structure:
    <output_path>/
    ├── sources.ipynb
    ├── entities.ipynb
    ├── concepts.ipynb
    └── syntheses.ipynb

Each notebook uses nbformat v4 schema and can be opened in Jupyter, VS Code,
or any .ipynb viewer.

CLI integration (not yet wired — add to cli.py as follows):
    # In the main() argument parser:
    # sub = subparsers.add_parser("export-jupyter",
    #                             help="Export wiki pages as Jupyter notebooks")
    # sub.add_argument("--wiki", default="wiki", help="Wiki directory")
    # sub.add_argument("--out", default="exports/jupyter", help="Output dir")
    # sub.set_defaults(func=cmd_export_jupyter)
    #
    # def cmd_export_jupyter(args):
    #     from llmwiki.export_jupyter import export_jupyter
    #     export_jupyter(Path(args.wiki), Path(args.out))
    #     return 0
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

# nbformat v4 constants
NBFORMAT = 4
NBFORMAT_MINOR = 5

# Sections to export (folder name -> notebook title)
SECTIONS = {
    "sources": "Sources",
    "entities": "Entities",
    "concepts": "Concepts",
    "syntheses": "Syntheses",
}


# ---------------------------------------------------------------------------
# Notebook cell builders
# ---------------------------------------------------------------------------


def _markdown_cell(source: str) -> dict[str, Any]:
    """Create a nbformat v4 markdown cell."""
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": _split_lines(source),
    }


def _code_cell(source: str, language: str = "") -> dict[str, Any]:
    """Create a nbformat v4 code cell."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": _split_lines(source),
    }


def _split_lines(text: str) -> list[str]:
    """Split text into the line list that nbformat expects.

    Each line (except the last) ends with a newline character.
    """
    if not text:
        return []
    lines = text.split("\n")
    result = []
    for i, line in enumerate(lines):
        if i < len(lines) - 1:
            result.append(line + "\n")
        elif line:  # skip trailing empty line
            result.append(line)
    return result


# ---------------------------------------------------------------------------
# Markdown -> cells parser
# ---------------------------------------------------------------------------

# Matches fenced code blocks: ```lang\n...\n```
_CODE_FENCE_RE = re.compile(
    r"^```(\w*)\s*\n(.*?)^```\s*$", re.MULTILINE | re.DOTALL
)


def _markdown_to_cells(content: str) -> list[dict[str, Any]]:
    """Split a markdown document into notebook cells.

    Fenced code blocks become code cells; everything else becomes
    markdown cells.
    """
    cells: list[dict[str, Any]] = []
    last_end = 0

    for match in _CODE_FENCE_RE.finditer(content):
        # Markdown before this code block
        before = content[last_end : match.start()].strip()
        if before:
            cells.append(_markdown_cell(before))

        lang = match.group(1) or ""
        code = match.group(2)
        cells.append(_code_cell(code, lang))
        last_end = match.end()

    # Trailing markdown after the last code block
    after = content[last_end:].strip()
    if after:
        cells.append(_markdown_cell(after))

    # If the document had no code blocks, it's a single markdown cell
    if not cells:
        cells.append(_markdown_cell(content.strip()))

    return cells


# ---------------------------------------------------------------------------
# Notebook builder
# ---------------------------------------------------------------------------


def _build_notebook(
    title: str, pages: list[tuple[str, str]]
) -> dict[str, Any]:
    """Build a complete nbformat v4 notebook from a list of (name, content) pages.

    Each page gets a heading cell followed by its parsed cells.
    """
    cells: list[dict[str, Any]] = []

    # Title cell
    cells.append(_markdown_cell(f"# {title}\n\nExported from llm-wiki."))

    for page_name, page_content in sorted(pages):
        # Section divider
        cells.append(_markdown_cell(f"---\n## {page_name}"))
        cells.extend(_markdown_to_cells(page_content))

    return {
        "nbformat": NBFORMAT,
        "nbformat_minor": NBFORMAT_MINOR,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "version": "3.11.0",
            },
        },
        "cells": cells,
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def export_jupyter(
    wiki_dir: str | Path, output_path: str | Path
) -> list[Path]:
    """Export wiki sections as Jupyter notebooks.

    Args:
        wiki_dir: Path to the wiki/ directory.
        output_path: Directory where .ipynb files are written.

    Returns:
        List of paths to the generated notebook files.
    """
    wiki_dir = Path(wiki_dir)
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    created: list[Path] = []

    for folder_name, nb_title in SECTIONS.items():
        section_dir = wiki_dir / folder_name
        if not section_dir.is_dir():
            continue

        pages: list[tuple[str, str]] = []
        for md in sorted(section_dir.glob("*.md")):
            if md.name.startswith("_"):
                continue
            try:
                content = md.read_text(encoding="utf-8")
            except OSError:
                continue
            # Strip YAML frontmatter
            content = _strip_frontmatter(content)
            pages.append((md.stem, content))

        if not pages:
            continue

        notebook = _build_notebook(nb_title, pages)
        nb_path = output_path / f"{folder_name}.ipynb"
        nb_path.write_text(
            json.dumps(notebook, indent=1, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        created.append(nb_path)

    return created


def _strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter (--- delimited) from the start of a document."""
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            return content[end + 4 :].lstrip("\n")
    return content
