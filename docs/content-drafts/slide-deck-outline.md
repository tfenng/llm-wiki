# Meetup Slide Deck Outline

**Target:** Python meetups, developer tooling meetups, AI/ML meetups
**Format:** 15 slides, ~20 minutes including demo
**Tool:** Any slide tool (Google Slides, Keynote, reveal.js, Marp)

---

## Slide 1 -- Title

**llm-wiki: Turn Your AI Coding Sessions Into a Searchable Knowledge Base**

- Your name
- Date
- GitHub: github.com/Pratiyush/llm-wiki
- Demo: pratiyush.github.io/llm-wiki

## Slide 2 -- The problem

**337 AI coding sessions. Never opened one.**

- Claude Code writes to `~/.claude/projects/`
- Copilot writes to VS Code workspace storage
- Cursor writes to its own store
- Codex CLI writes to `~/.codex/sessions/`
- Gemini CLI writes to `~/.gemini/`

Five tools. Five stores. Zero search. Zero cross-referencing.

Your AI coding knowledge is write-once, read-never.

## Slide 3 -- What is in those transcripts

- Architecture decisions you discussed with the AI
- Debugging sessions, including the dead ends
- Library evaluations and trade-off analyses
- Code snippets you will want again
- Tool usage patterns you have never examined

This is valuable. It is just inaccessible.

## Slide 4 -- The Karpathy LLM Wiki pattern

**Three layers:**

```
raw/    -- Immutable source transcripts
wiki/   -- LLM-maintained knowledge pages
site/   -- Generated static HTML
```

From Andrej Karpathy's gist (link). Each layer has one owner. No layer reaches back to modify an earlier one.

## Slide 5 -- llm-wiki in 30 seconds

```bash
git clone https://github.com/Pratiyush/llm-wiki.git
cd llm-wiki && ./setup.sh
./sync.sh       # JSONL -> markdown
./build.sh      # markdown -> HTML
./serve.sh      # browse at localhost:8765
```

No npm. No database. No API key. Python 3.9+ and `markdown`.

## Slide 6 -- LIVE DEMO: Home page

[Switch to browser]

- Activity heatmap (365-day, GitHub-style)
- Token usage stat cards
- Project grid with topic chips
- Recently-updated card

## Slide 7 -- LIVE DEMO: Search and navigation

- Cmd+K command palette (fuzzy search)
- Keyboard shortcuts: `g h` / `g p` / `g s` / `j` / `k`
- Filter bar on sessions table
- Wikilink hover previews

## Slide 8 -- LIVE DEMO: Session detail

- Full conversation with syntax highlighting (highlight.js)
- Tool-calling bar chart (pure SVG)
- Token usage card with cache-hit ratio
- Breadcrumbs, reading time, related pages
- Copy-as-markdown button

## Slide 9 -- LIVE DEMO: Model directory

- Sortable model table with benchmarks
- Per-model detail page with info card
- Auto-generated vs-comparison pages
- Append-only changelog timeline with pricing sparkline

## Slide 10 -- Architecture: the adapter pattern

```
BaseAdapter
  |-- claude_code.py    (~60 lines)
  |-- codex_cli.py      (~55 lines)
  |-- copilot_chat.py   (~70 lines)
  |-- cursor.py         (~65 lines)
  |-- gemini_cli.py     (~60 lines)
  +-- obsidian.py       (~50 lines)
```

Each adapter knows: where the agent stores sessions, how to discover them, how to derive a project slug.

Everything else (parsing, filtering, redaction, rendering) is shared in `convert.py`.

Adding a new agent = 1 file + 1 fixture + 1 test.

## Slide 11 -- Architecture: the build pipeline

```
build.py (one file)
  |-- Discover .md files
  |-- Parse frontmatter + body
  |-- Aggregate per-project stats
  |-- Generate computed data (heatmaps, charts)
  |-- Render HTML with f-strings + markdown lib
  |-- Write to site/
  +-- Generate AI exports (llms.txt, JSON-LD, .txt/.json siblings)
```

No Jinja. No template engine. CSS and JS are string constants.

Why? Because the input is structured data, not blog posts. A template language would fight the data pipeline.

## Slide 12 -- Pure-SVG visualizations

Four modules, all stdlib Python generating SVG strings:

| Module | What it renders |
|---|---|
| `viz_heatmap.py` | 365-day activity grid |
| `viz_tools.py` | Tool-calling bar charts |
| `viz_tokens.py` | Token usage stacked bars |
| `changelog_timeline.py` | Model changelog + pricing sparkline |

- No D3, Chart.js, or Matplotlib
- CSS custom properties for dark mode
- Prints cleanly, works in RSS readers
- Zero JavaScript required

## Slide 13 -- AI-consumable dual format

Every page ships in three formats:

| Format | Audience |
|---|---|
| `.html` | Humans (with Schema.org microdata) |
| `.txt` | LLMs (plain text, no tags) |
| `.json` | Agents (structured metadata + body) |

Site-level exports: `llms.txt`, `llms-full.txt`, `graph.jsonld`, `sitemap.xml`, `rss.xml`

MCP server: 7 tools. Claude Desktop, Cursor, or any MCP client can query your wiki.

## Slide 14 -- Design principles

1. **Stdlib-only** -- one runtime dep (`markdown`). No npm. No bundler.
2. **Privacy by default** -- auto-redaction, localhost-only, no telemetry, `.llmwikiignore`
3. **Idempotent** -- re-running any command is safe and cheap
4. **Agent-agnostic** -- core does not know which agent produced the data
5. **Dual-format** -- every page for humans AND machines
6. **472 tests** -- unit + Playwright E2E + snapshot tests

## Slide 15 -- Try it / contribute

**5-minute setup:**
```bash
git clone https://github.com/Pratiyush/llm-wiki.git
cd llm-wiki && ./setup.sh
./build.sh && ./serve.sh
```

**Links:**
- Live demo: pratiyush.github.io/llm-wiki
- GitHub: github.com/Pratiyush/llm-wiki
- Karpathy's spec: gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

**Contribute:**
- Add an adapter for your favorite agent (one file)
- Report bugs or request features
- Star the repo

MIT license. Works offline. Your AI sessions deserve better than /dev/null.

---

## Speaker notes

- Slides 6-9 are live demo. Have the demo site pre-loaded at localhost:8765 as a fallback in case of network issues (the demo site also works from the GitHub Pages URL if you want to show the public version).
- For the adapter pattern slide, emphasize the ~50-line file size -- this is what makes the project approachable for contributors.
- For the SVG slide, consider opening the browser inspector to show that the heatmap is just `<rect>` elements with CSS custom properties.
- Time budget: slides 1-5 (5 min), demo slides 6-9 (7 min), architecture slides 10-14 (6 min), CTA slide 15 (2 min).
