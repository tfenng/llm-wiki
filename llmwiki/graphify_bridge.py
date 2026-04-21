"""Graphify integration bridge for llmwiki.

Delegates graph building, community detection, and analysis to the
``graphifyy`` package (https://github.com/safishamsi/graphify) when
installed.  Falls back gracefully when not available.

Install:  pip install graphifyy          # or: pip install llmwiki[graph]
Extras:   pip install graphifyy[mcp]     # MCP server
          pip install graphifyy[leiden]   # better community detection

Usage from CLI:
    python3 -m llmwiki graph --engine graphify

Usage from Python:
    from llmwiki.graphify_bridge import is_available, build_graphify_graph
    if is_available():
        result = build_graphify_graph()
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from llmwiki import REPO_ROOT

WIKI_DIR = REPO_ROOT / "wiki"
GRAPH_DIR = REPO_ROOT / "graph"
GRAPHIFY_OUT = REPO_ROOT / "graphify-out"


def is_available() -> bool:
    """Return True when graphifyy is importable."""
    try:
        import graphify  # noqa: F401
        return True
    except ImportError:
        return False


def build_graphify_graph(
    *,
    scan_paths: list[Path] | None = None,
    directed: bool = False,
    mode: str = "default",
    update_only: bool = False,
) -> dict[str, Any]:
    """Run the Graphify pipeline on the wiki (and optionally source code).

    Parameters
    ----------
    scan_paths : list[Path] | None
        Paths to scan. Defaults to ``[wiki/, llmwiki/]``.
    directed : bool
        Use directed graph (preserves edge direction).
    mode : str
        Extraction mode: "default" or "deep" (aggressive inference).
    update_only : bool
        Only re-extract changed files (incremental).

    Returns
    -------
    dict with keys: graph (NetworkX), communities, gods, report_path,
    json_path, html_path, stats.
    """
    from graphify.detect import detect
    from graphify.extract import extract
    from graphify.build import build_from_json
    from graphify.cluster import cluster, score_all
    from graphify.analyze import god_nodes, surprising_connections, suggest_questions
    from graphify.report import generate as generate_report
    from graphify.export import to_json, to_html

    if scan_paths is None:
        scan_paths = [WIKI_DIR]
        # Also scan source code if it exists
        src_dir = REPO_ROOT / "llmwiki"
        if src_dir.is_dir():
            scan_paths.append(src_dir)

    # Step 1: Detect files
    all_files: list[Path] = []
    for sp in scan_paths:
        result = detect(sp)
        for category in result.get("files", {}).values():
            all_files.extend(Path(f) for f in category)

    if not all_files:
        print("  warning: no files found to graph", file=sys.stderr)
        return {"graph": None, "stats": {"total_nodes": 0, "total_edges": 0}}

    print(f"  graphify: detected {len(all_files)} files across {len(scan_paths)} paths")

    # Step 2: Extract (AST for code, semantic for docs)
    code_files = [f for f in all_files if f.suffix in {
        ".py", ".ts", ".js", ".go", ".rs", ".java", ".cpp", ".c", ".rb",
    }]
    doc_files = [f for f in all_files if f.suffix in {".md", ".mdx", ".txt", ".rst"}]

    extraction: dict[str, Any] = {"nodes": [], "edges": []}

    if code_files:
        print(f"  graphify: extracting {len(code_files)} code files (AST, no LLM)...")
        code_ext = extract(code_files, cache_root=GRAPHIFY_OUT)
        extraction["nodes"].extend(code_ext.get("nodes", []))
        extraction["edges"].extend(code_ext.get("edges", []))

    # For docs, we use AST extraction too (Graphify handles .md files)
    if doc_files:
        print(f"  graphify: extracting {len(doc_files)} doc files...")
        doc_ext = extract(doc_files, cache_root=GRAPHIFY_OUT)
        extraction["nodes"].extend(doc_ext.get("nodes", []))
        extraction["edges"].extend(doc_ext.get("edges", []))

    if not extraction["nodes"]:
        print("  warning: no nodes extracted", file=sys.stderr)
        return {"graph": None, "stats": {"total_nodes": 0, "total_edges": 0}}

    print(f"  graphify: {len(extraction['nodes'])} nodes, {len(extraction['edges'])} edges extracted")

    # Step 3: Build NetworkX graph
    G = build_from_json(extraction, directed=directed)

    # Step 4: Community detection
    communities = cluster(G)
    cohesion = score_all(G, communities)
    print(f"  graphify: {len(communities)} communities detected")

    # Step 5: Analysis
    gods = god_nodes(G, top_n=10)
    surprises = surprising_connections(G, communities)
    questions = suggest_questions(G, communities)

    # Step 6: Generate report
    report_md = generate_report(
        G, communities, cohesion,
        gods=gods,
        surprises=surprises,
        suggested_questions=questions,
        project_path=str(REPO_ROOT),
    )

    # Step 7: Export
    GRAPHIFY_OUT.mkdir(parents=True, exist_ok=True)
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)

    # Write to graphify-out/
    json_path = GRAPHIFY_OUT / "graph.json"
    html_path = GRAPHIFY_OUT / "graph.html"
    report_path = GRAPHIFY_OUT / "GRAPH_REPORT.md"

    to_json(G, communities, str(json_path))
    to_html(G, communities, str(html_path))
    report_path.write_text(report_md, encoding="utf-8")

    # Also copy to graph/ for compatibility with existing build pipeline
    graph_json = GRAPH_DIR / "graph.json"
    graph_html = GRAPH_DIR / "graph.html"
    graph_json.write_text(json_path.read_text(encoding="utf-8"), encoding="utf-8")
    graph_html.write_text(html_path.read_text(encoding="utf-8"), encoding="utf-8")

    stats = {
        "total_nodes": G.number_of_nodes(),
        "total_edges": G.number_of_edges(),
        "communities": len(communities),
        "god_nodes": [g["label"] if isinstance(g, dict) else str(g) for g in gods[:5]],
    }

    print(f"  graphify: wrote {json_path.relative_to(REPO_ROOT)}")
    print(f"  graphify: wrote {html_path.relative_to(REPO_ROOT)}")
    print(f"  graphify: wrote {report_path.relative_to(REPO_ROOT)}")
    print(f"  graphify: {stats['total_nodes']} nodes, {stats['total_edges']} edges, "
          f"{stats['communities']} communities")

    if gods:
        print("  graphify: god nodes (most connected):")
        for g in gods[:5]:
            label = g["label"] if isinstance(g, dict) else str(g)
            print(f"    - {label}")

    return {
        "graph": G,
        "communities": communities,
        "cohesion": cohesion,
        "gods": gods,
        "surprises": surprises,
        "questions": questions,
        "report_path": report_path,
        "json_path": json_path,
        "html_path": html_path,
        "stats": stats,
    }


def export_obsidian(vault_path: Path | None = None) -> Path:
    """Export the Graphify graph to Obsidian vault format."""
    from graphify.export import to_obsidian, to_canvas

    json_path = GRAPHIFY_OUT / "graph.json"
    if not json_path.is_file():
        raise FileNotFoundError(
            f"No graph found at {json_path}. Run `llmwiki graph --engine graphify` first."
        )

    # Load graph
    import networkx as nx
    from networkx.readwrite import json_graph
    data = json.loads(json_path.read_text(encoding="utf-8"))
    G = json_graph.node_link_graph(data, edges="links")

    # Extract communities from node attributes
    communities: dict[int, list[str]] = {}
    for nid, ndata in G.nodes(data=True):
        cid = ndata.get("community", 0)
        communities.setdefault(cid, []).append(nid)

    target = vault_path or GRAPHIFY_OUT / "obsidian"
    to_obsidian(G, communities, str(target))
    to_canvas(G, communities, str(target / "graph.canvas"))

    print(f"  graphify: obsidian vault written to {target}")
    return target


def export_wiki() -> Path:
    """Export the Graphify graph as an agent-crawlable wiki."""
    from graphify.export import to_wiki

    json_path = GRAPHIFY_OUT / "graph.json"
    if not json_path.is_file():
        raise FileNotFoundError(
            f"No graph found at {json_path}. Run `llmwiki graph --engine graphify` first."
        )

    import networkx as nx
    from networkx.readwrite import json_graph
    data = json.loads(json_path.read_text(encoding="utf-8"))
    G = json_graph.node_link_graph(data, edges="links")

    communities: dict[int, list[str]] = {}
    for nid, ndata in G.nodes(data=True):
        cid = ndata.get("community", 0)
        communities.setdefault(cid, []).append(nid)

    target = GRAPHIFY_OUT / "wiki"
    to_wiki(G, communities, str(target))

    print(f"  graphify: wiki written to {target}")
    return target


def query_graph(question: str, *, mode: str = "bfs", depth: int = 3,
                token_budget: int = 2000) -> str:
    """Query the knowledge graph with a natural language question.

    Uses Graphify's BFS/DFS traversal to find relevant subgraph nodes,
    then returns a text summary within the token budget.
    """
    from graphify.serve import _load_graph, _score_nodes, _bfs, _dfs, _subgraph_to_text

    json_path = GRAPHIFY_OUT / "graph.json"
    if not json_path.is_file():
        return f"No graph found. Run `llmwiki graph --engine graphify` first."

    G = _load_graph(str(json_path))
    keywords = question.lower().split()
    scored = _score_nodes(G, keywords)

    if not scored:
        return "No matching nodes found in the knowledge graph."

    # Use top scored nodes as seeds
    seed_ids = [nid for _, nid in scored[:3]]

    if mode == "dfs":
        nodes, edges = _dfs(G, seed_ids, depth=depth)
    else:
        nodes, edges = _bfs(G, seed_ids, depth=depth)

    return _subgraph_to_text(G, nodes, edges, token_budget=token_budget)
