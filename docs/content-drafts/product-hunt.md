# Product Hunt Launch Copy

**Target:** Product Hunt
**Tone:** Clear, benefit-focused, concise

---

## Tagline (60 chars max)

Turn your AI coding sessions into a searchable knowledge base

## Description (260 chars max)

llm-wiki converts transcripts from Claude Code, Copilot, Cursor, Codex CLI, and Gemini CLI into a beautiful static wiki. Activity heatmaps, tool charts, model comparisons, Cmd+K search. Local, free, open-source. Based on Karpathy's LLM Wiki pattern.

## Longer description

Every AI coding assistant writes full session transcripts to disk. You have hundreds of them. You never look at them again.

llm-wiki turns that dormant history into a searchable, interlinked knowledge base you can browse locally or deploy as a static site.

**What it does:**

- Converts JSONL transcripts from 6+ AI agents into clean, redacted markdown
- Builds a static HTML site with global search (Cmd+K), dark mode, syntax highlighting, and keyboard shortcuts
- Generates 365-day activity heatmaps, tool-calling bar charts, token usage cards, and AI model comparison pages
- Ships machine-readable exports (llms.txt, JSON-LD, per-page .txt/.json) so other AI tools can query your wiki
- Includes an MCP server with 7 tools for live querying from Claude Desktop or Cursor

**What makes it different:**

- Works with Claude Code, Codex CLI, Copilot, Cursor, Gemini CLI, and Obsidian in one unified wiki
- All visualizations are pure SVG -- no JavaScript charting library
- Stdlib-only Python (one dependency: `markdown`)
- Follows Andrej Karpathy's three-layer LLM Wiki architecture
- Privacy-first: everything local, automatic redaction, no telemetry, no cloud
- 472 tests, MIT license, active development (9 releases)

**Setup:**

```
git clone https://github.com/Pratiyush/llm-wiki.git
cd llm-wiki && ./setup.sh
./build.sh && ./serve.sh
```

## First Comment (from maker)

Hey Product Hunt! I built llm-wiki because I had 337 AI coding sessions across Claude Code, Copilot, and Cursor that I never looked at after they ended. That felt like a waste -- those transcripts contain architecture decisions, debugging patterns, library evaluations, and code snippets that are genuinely valuable.

The core idea comes from Andrej Karpathy's LLM Wiki gist: a three-layer architecture where raw transcripts feed an LLM-maintained wiki that compiles into a static site.

Some technical decisions I am proud of:

- The adapter pattern makes adding new agents trivial (one 50-line file each)
- All charts are pure SVG generated at build time -- no D3, no Chart.js, just Python stdlib generating strings
- Every page ships in three formats: HTML for you, .txt and .json for AI agents
- The entire site generator is one Python file with f-strings. No template engine.

I'd love feedback on the demo site (built from synthetic sessions, no personal data): https://pratiyush.github.io/llm-wiki/

The project is MIT licensed and the whole setup takes about 5 minutes. No API key needed, everything runs locally.

What AI coding assistants do you use? I'm curious which adapters to prioritize next.

## Maker Story

I use AI coding assistants 8+ hours a day. Claude Code for complex refactoring, Copilot for quick completions, Cursor for prototyping. After a year, I had hundreds of session transcripts scattered across five different tools in raw JSONL format.

One day I needed to recall how I had solved a specific WebSocket reconnection issue. I knew I had discussed it with Claude Code months ago, but I could not find it. I spent 20 minutes grep-ing through JSONL files before giving up.

That was the moment I decided to build llm-wiki. The session transcripts were already there -- I just needed a way to make them accessible.

Karpathy's LLM Wiki gist provided the architecture. Nine releases later, it supports six AI agents, generates pure-SVG visualizations, ships AI-consumable exports, and runs entirely on your local machine with zero cloud dependencies.

## Topics/Categories

- Developer Tools
- Artificial Intelligence
- Open Source
- Productivity
- Knowledge Management

## Links

- Website: https://pratiyush.github.io/llm-wiki/
- GitHub: https://github.com/Pratiyush/llm-wiki

## Gallery images (suggested)

1. `docs/images/home.png` -- Home page with activity heatmap
2. `docs/images/sessions.png` -- Sessions index with filter bar
3. `docs/images/session-rust.png` -- Session detail with syntax highlighting
4. `docs/images/projects.png` -- Projects index with freshness badges
5. `docs/images/model.png` -- Model info card
6. `docs/images/compare.png` -- Model comparison page
