# How llm-wiki Turns JSONL Into a Knowledge Base

**Target:** Dev blog, Hashnode, dev.to, HN-adjacent audience
**Length:** ~2,000 words
**Tone:** Technical, implementation-focused

---

[llm-wiki](https://github.com/Pratiyush/llm-wiki) converts raw AI coding session transcripts into a searchable, interlinked static site. This post walks through the architecture -- from JSONL parsing to pure-SVG visualizations -- and explains why every design decision leans toward simplicity.

## The three-layer Karpathy architecture

The project follows [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), which prescribes three distinct layers:

**Layer 1 -- Raw (`raw/`).** Immutable source documents. The converter reads `.jsonl` from your agent's session store, filters noise, runs redaction, and writes one markdown file per session to `raw/sessions/<project>/<date>-<slug>.md`. Each file has rich YAML frontmatter: project, model, tools_used, token_totals, tool_counts, duration_seconds, and more. This layer is never modified after initial conversion.

**Layer 2 -- Wiki (`wiki/`).** LLM-maintained pages. Your coding agent (Claude Code, Codex, etc.) reads the raw layer and produces structured wiki pages: source summaries, entity pages (people, projects, tools), concept pages (patterns, decisions, frameworks), comparisons, syntheses. Everything is interlinked with `[[wikilinks]]`. Contradictions between sources are flagged, not silently overwritten.

**Layer 3 -- Site (`site/`).** Generated static HTML. The build pipeline reads both layers and produces a complete website you can browse locally or deploy anywhere.

The key insight is that each layer has a single owner. The converter owns `raw/`. The LLM owns `wiki/`. The build script owns `site/`. No layer reaches back to modify an earlier one.

## The adapter pattern: one file per agent

Claude Code writes `.jsonl` to `~/.claude/projects/`. Codex CLI writes to `~/.codex/sessions/`. Cursor stores session data in VS Code's workspace storage. Gemini CLI uses `~/.gemini/`. Each format is slightly different.

The adapter pattern keeps this complexity isolated. Every agent gets one file at `llmwiki/adapters/<agent>.py` that subclasses `BaseAdapter` and implements three things:

1. **Where** the agent stores sessions (platform-aware paths for macOS/Linux/Windows)
2. **How** to discover `.jsonl` files in that store
3. **How** to derive a project slug from the file path

Everything else -- record parsing, filtering, redaction, markdown rendering -- lives in the shared `convert.py`. The adapters are thin translation layers, typically 50-100 lines each.

Adding a new agent is one file, one fixture, one snapshot test, one doc page, one README line, one CHANGELOG entry. The Copilot adapter (both Chat and CLI variants) was shipped in a single PR.

Currently supported: Claude Code (v0.1), Obsidian (v0.1), Codex CLI (v0.3), Cursor (v0.5), Gemini CLI (v0.5), PDF (v0.5), Copilot Chat (v0.9), Copilot CLI (v0.9).

## The build pipeline: markdown to HTML

`llmwiki build` is a single Python module (`build.py`) that reads every `.md` file under `raw/` and renders a complete static site. The entire HTML generation -- templates, CSS, JavaScript -- lives in one file. No Jinja. No template engine. Python f-strings and the stdlib `markdown` library.

The build produces:

- **Home page** with a hero section, 365-day activity heatmap, token usage stats, recently-updated card, and project grid with topic chips
- **Project pages** with scoped heatmaps, tool-calling bar charts, token timelines, and session lists
- **Session pages** with the full conversation, breadcrumbs, reading time, code highlighting, related pages panel, and copy-as-markdown buttons
- **Model directory** with sortable benchmark tables and per-model detail pages
- **Comparison pages** auto-generated from model pairs that share enough structured data
- **Changelog page** rendering `CHANGELOG.md` as a first-class page
- **Search index** -- a pre-built JSON file consumed by the client-side command palette

The CSS uses custom properties (`--bg`, `--text`, `--accent`, etc.) for theming. Dark mode is system-aware with a manual toggle that persists to `localStorage`. Print styles are included. WCAG 2.1 AA contrast compliance was verified with axe-core.

The JavaScript is vanilla. Zero dependencies. No framework. No bundler. It handles the theme toggle, command palette, keyboard shortcuts, filter bar, copy buttons, collapsible sections, and reading progress bar. The whole thing is a string constant embedded in `build.py`.

## AI-consumable dual format

Since v0.4, every HTML page has two machine-readable siblings at the same URL:

- `<page>.txt` -- plain text, no HTML tags, for pasting into any LLM's context
- `<page>.json` -- structured metadata + body + SHA-256 hash + outbound wikilinks

Site-level exports include:

- `llms.txt` / `llms-full.txt` per the [llmstxt.org spec](https://llmstxt.org)
- `graph.jsonld` -- Schema.org JSON-LD entity graph
- `sitemap.xml`, `rss.xml`, `robots.txt`
- `manifest.json` with SHA-256 hashes and performance budget checks
- `ai-readme.md` explaining the structure for AI agents

Every HTML page also includes an `<!-- llmwiki:metadata -->` comment block and Schema.org microdata (`itemscope`, `datePublished`, etc.) so crawlers and AI agents can parse structure without fetching the JSON sibling.

There is also an MCP server (`python3 -m llmwiki.mcp`) with 7 tools (`wiki_query`, `wiki_search`, `wiki_list_sources`, `wiki_read_page`, `wiki_lint`, `wiki_sync`, `wiki_export`) so Claude Desktop, Cursor, or any MCP client can query the wiki live.

## Pure-SVG build-time visualizations

The visualization layer is the part I am most proud of from an engineering standpoint. Four modules render data as pure SVG at build time:

**`viz_heatmap.py`** -- A 365-day activity grid, like GitHub's contribution graph. Sunday-aligned, 53 columns, five-level quantile bucketing computed over non-zero days. Renders both a global aggregate on the home page and per-project scoped views.

**`viz_tools.py`** -- Horizontal bar charts of tool usage. Category-based coloring (I/O tools are blue, search tools are purple, execution tools are orange, network tools are green). Top 10 tools with an overflow row. Per-session and per-project aggregate views.

**`viz_tokens.py`** -- Token usage cards with stacked bars (input, cache creation, cache read, output) and cache-hit-ratio badges. Project-level timeline as a log-scale area chart. Site-wide stat cards.

**`changelog_timeline.py`** -- Vertical timeline for model entity changelogs. Color-coded deltas (price cuts green, hikes red, benchmark lifts green). Pricing sparkline SVG when enough data points exist.

Every visualization is stdlib-only Python generating SVG strings. No D3. No Chart.js. No Matplotlib. The SVG is inlined directly into the HTML at build time, so it renders instantly with zero JavaScript, works in RSS readers and plain-text email clients, and prints cleanly.

Dark mode variants are handled entirely through CSS custom properties (`--heatmap-0..4`, `--tool-cat-io`, `--token-input`, etc.) applied to the same SVG markup.

## The stdlib-only philosophy

The only mandatory runtime dependency is Python's `markdown` library. Everything else is stdlib:

- `http.server` for the local dev server
- `json` for `.jsonl` parsing and search index generation
- `hashlib` for content-addressable image filenames and manifest hashes
- `urllib.request` for image downloads
- `xml.etree` for sitemap and RSS generation
- `pathlib` for all file operations
- `re` for redaction patterns

Optional extras: `pypdf` for PDF ingestion, `pytest` + `ruff` for development, `playwright` + `pytest-bdd` for E2E testing.

Why? Because every dependency is a maintenance burden, a security surface, and a barrier to contribution. `pip install -e .` should work on a fresh Python 3.9 install with no compilation step and no C extensions.

Syntax highlighting is the one place where a fully client-side approach won out. highlight.js loads from a pinned CDN at view time, with two preloaded theme stylesheets (GitHub light and GitHub dark) that swap on theme toggle. The build stays deterministic and offline-capable -- if the CDN is unreachable, code blocks render as plain monospace text.

## Testing

472 unit tests run in milliseconds and cover every module. The E2E suite (separate, opt-in) builds a minimal demo site, serves it on a random port, and drives a real Chromium browser via Playwright. 62 scenarios written in Gherkin cover the command palette, keyboard navigation, theme toggle, responsive layout, accessibility, and visual regression.

The test pyramid is strict: unit tests lock the contract at the module boundary, E2E locks it at the browser. A diff that passes unit tests but breaks the command palette will fail E2E.

## Try it yourself

```bash
git clone https://github.com/Pratiyush/llm-wiki.git
cd llm-wiki && ./setup.sh
./build.sh && ./serve.sh
```

Or browse the [live demo](https://pratiyush.github.io/llm-wiki/) to see it running against synthetic sessions.

**Links:**
- GitHub: [github.com/Pratiyush/llm-wiki](https://github.com/Pratiyush/llm-wiki)
- Live demo: [pratiyush.github.io/llm-wiki](https://pratiyush.github.io/llm-wiki/)
- Architecture docs: [github.com/Pratiyush/llm-wiki/blob/master/docs/architecture.md](https://github.com/Pratiyush/llm-wiki/blob/master/docs/architecture.md)
