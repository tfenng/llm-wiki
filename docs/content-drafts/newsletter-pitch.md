# Newsletter Pitch

**Target:** Python Weekly, TLDR, tl;dr sec, Console.dev, Changelog, Benedict Evans, AI Tidbits, The Batch, Hacker Newsletter
**Length:** Short -- one paragraph + links
**Tone:** Factual, no hype

---

## Subject line options

- "llm-wiki: Turn AI coding sessions into a searchable knowledge base"
- "Open-source tool converts Claude Code/Copilot/Cursor sessions into a local wiki"
- "Karpathy-pattern LLM Wiki for AI coding assistants (Python, MIT, stdlib-only)"

## Pitch (Python Weekly / TLDR)

**llm-wiki** is an open-source Python tool that converts session transcripts from Claude Code, Copilot, Cursor, Codex CLI, and Gemini CLI into a searchable, interlinked static website. It follows Andrej Karpathy's three-layer LLM Wiki architecture (raw sources, LLM-maintained wiki, generated HTML) and supports 6+ AI agents via a pluggable adapter pattern. The build pipeline produces pure-SVG visualizations (activity heatmaps, tool charts, token usage cards), AI-consumable exports (llms.txt, JSON-LD, per-page .txt/.json), and an MCP server for live querying. Stdlib-only (one dep: `markdown`). No cloud, no API key, privacy-first with automatic redaction. MIT license, 472 tests, active development.

GitHub: https://github.com/Pratiyush/llm-wiki
Live demo: https://pratiyush.github.io/llm-wiki/
Karpathy's spec: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

## Pitch (Console.dev / Changelog -- shorter)

**llm-wiki** converts AI coding session transcripts (Claude Code, Copilot, Cursor, Codex, Gemini) into a searchable static wiki. Follows Karpathy's LLM Wiki pattern. Pure-SVG visualizations, multi-agent support, AI-consumable exports, MCP server. Python stdlib-only, MIT license, everything runs locally.

GitHub: https://github.com/Pratiyush/llm-wiki
Demo: https://pratiyush.github.io/llm-wiki/

## Pitch (tl;dr sec -- security angle)

**llm-wiki** is an open-source tool for archiving AI coding sessions locally. Privacy-first: automatic redaction of usernames, API keys, tokens, and emails before data hits disk. `.llmwikiignore` for project exclusions. Localhost-only binding. No telemetry, no cloud calls, no accounts. Supports Claude Code, Copilot, Cursor, Codex CLI, Gemini CLI. MIT license.

GitHub: https://github.com/Pratiyush/llm-wiki

## Pitch (AI-focused newsletters -- The Batch, AI Tidbits)

**llm-wiki** implements Andrej Karpathy's LLM Wiki pattern specifically for AI coding assistants. It converts session transcripts from 6+ agents (Claude Code, Copilot, Cursor, Codex CLI, Gemini CLI) into a three-layer knowledge base: immutable raw transcripts, LLM-maintained wiki pages with wikilinks, and a static HTML site with search and visualizations. Every page ships as both human-readable HTML and machine-readable formats (.txt, .json, JSON-LD, llms.txt), with an MCP server for live querying. Open-source, stdlib-only Python, runs entirely local.

GitHub: https://github.com/Pratiyush/llm-wiki
Demo: https://pratiyush.github.io/llm-wiki/
