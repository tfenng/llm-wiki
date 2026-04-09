# Twitter/X Launch Thread (5 tweets)

**Target:** Twitter/X
**Tone:** Concise, technical, demo-forward

---

## Tweet 1 -- Hook + demo link

I built a tool that turns your AI coding sessions into a searchable wiki.

Every Claude Code, Copilot, Cursor, and Codex session you've ever run -- unified, searchable, visualized.

Live demo: https://pratiyush.github.io/llm-wiki/

Thread on how it works:

## Tweet 2 -- What it does

llm-wiki follows @karpathy's LLM Wiki architecture:

1. JSONL transcripts -> clean markdown (redacted, with rich frontmatter)
2. LLM-maintained wiki pages (entities, concepts, cross-links)
3. Static HTML site with Cmd+K search, dark mode, syntax highlighting

Two commands: sync + build. No npm. No database. Python stdlib only.

## Tweet 3 -- Multi-agent support

Supports 6+ AI coding agents:

- Claude Code
- Codex CLI
- GitHub Copilot (Chat + CLI)
- Cursor
- Gemini CLI
- Obsidian

Colored agent badges so you can tell who said what. One pluggable adapter per agent (~50 lines of Python each).

## Tweet 4 -- Features

The site ships with:

- 365-day activity heatmap (GitHub-style)
- Tool-calling bar charts per session + project
- Token usage cards with cache-hit ratios
- AI model directory with auto-generated vs-comparisons
- Pricing sparklines from append-only changelogs

All pure SVG. No JS charting libraries. Built at compile time.

[Attach: docs/images/home.png or docs/images/llmwiki-combined-4up.png]

## Tweet 5 -- CTA

llm-wiki is MIT licensed. Works offline. No API key.

Every page ships as HTML + .txt + .json for AI agents. Includes an MCP server and llms.txt exports.

472 tests. 9 releases. 161 features tracked.

GitHub: https://github.com/Pratiyush/llm-wiki
Demo: https://pratiyush.github.io/llm-wiki/

Star it if your AI session history deserves better than /dev/null.
