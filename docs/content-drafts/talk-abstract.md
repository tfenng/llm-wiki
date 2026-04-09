# Conference Lightning Talk Abstract (5 min)

**Target:** PyCon, local Python meetups, AI/ML conferences, developer tooling conferences
**Format:** Lightning talk (5 minutes)

---

## Title

From JSONL to Knowledge Base: Building a Wiki From Your AI Coding Sessions

## Abstract (200 words)

Every AI coding assistant -- Claude Code, Copilot, Cursor, Codex CLI, Gemini CLI -- writes full session transcripts to disk. Developers accumulate hundreds of these, then never look at them again. The result: thousands of hours of architecture decisions, debugging sessions, and code reviews evaporate after each session ends.

llm-wiki is an open-source Python tool that turns this dormant history into a searchable, interlinked knowledge base. It follows Andrej Karpathy's three-layer LLM Wiki architecture to convert raw JSONL transcripts into a beautiful static site with global search, pure-SVG visualizations, and machine-readable exports.

In this lightning talk, I will demonstrate the three-layer pipeline (raw, wiki, site), show how the pluggable adapter pattern supports 6+ AI agents in one unified view, and walk through the stdlib-only design decisions that keep the project at one runtime dependency. I will also show the pure-SVG visualization approach (activity heatmaps, tool charts, token usage cards) and the dual-format output that makes every page readable by both humans and AI agents.

Attendees will leave understanding how to set up their own AI coding knowledge base in 5 minutes and how the adapter pattern makes it extensible.

## Bio

[Customize with your name and background]

Open-source developer and maintainer of llm-wiki, a Python tool for converting AI coding session transcripts into searchable knowledge bases. Works daily with Claude Code, Copilot, and Cursor. Interested in developer tooling, knowledge management, and the intersection of AI assistants and software engineering workflows.

## Outline (5 minutes)

**0:00 -- 0:30 | The problem (30s)**
- Show: 337 JSONL files on disk. Never opened one.
- "Write-once, read-never" -- the AI session transcript graveyard.

**0:30 -- 1:15 | The Karpathy pattern (45s)**
- Karpathy's gist: three layers (raw, wiki, site)
- Why immutability matters at the raw layer
- Why the wiki layer needs an LLM in the loop

**1:15 -- 2:15 | Live demo (60s)**
- `./build.sh && ./serve.sh` on the demo data
- Home page: activity heatmap, project grid
- Cmd+K: fuzzy search across everything
- Session detail: syntax highlighting, tool chart, token card
- Model comparison page

**2:15 -- 3:15 | Architecture (60s)**
- Adapter pattern: one file per agent, shared core
- build.py: one file, f-strings, no template engine
- Pure-SVG charts: viz_heatmap.py, viz_tools.py, viz_tokens.py
- CSS custom properties for theming (light + dark in one SVG)

**3:15 -- 4:00 | AI-consumable output (45s)**
- Every page: .html + .txt + .json
- Site-level: llms.txt, JSON-LD, sitemap, RSS
- MCP server: 7 tools, any MCP client can query your wiki
- "Your wiki is not just for your eyes"

**4:00 -- 4:30 | Design principles (30s)**
- Stdlib-only (one dep: `markdown`)
- Privacy by default (redaction, localhost, no telemetry)
- 472 tests, Playwright E2E, MIT license

**4:30 -- 5:00 | CTA (30s)**
- `git clone` + `./setup.sh` -- 5 minutes
- Live demo URL
- GitHub URL
- "Your AI sessions deserve better than /dev/null"

## Requirements

- Screen/projector for live demo
- Internet not required (demo runs locally)
- No special software needed in the room

## Format preferences

- Lightning talk: 5 minutes (ideal)
- Short talk: 10 minutes (expanded demo + audience Q&A)
- Full talk: 25 minutes (add: deep-dive on adapter pattern, SVG visualization pipeline, testing strategy)
