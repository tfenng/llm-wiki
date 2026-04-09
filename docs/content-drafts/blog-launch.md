# I Built a Wiki From My AI Coding Sessions

**Target:** Dev blog, Hashnode, dev.to, personal blog
**Length:** ~1,500 words
**Tone:** Personal, developer-to-developer

---

Every developer using Claude Code, Copilot, Cursor, or Codex CLI has hundreds of session transcripts sitting on their hard drive right now. Full conversations with an AI about architecture decisions, debugging sessions, code reviews, library evaluations. Thousands of hours of context that you will never look at again.

I had 337 of them. I never opened a single one after the session ended.

That bothered me, so I built [llm-wiki](https://github.com/Pratiyush/llm-wiki).

## The problem: write-once, read-never

Every AI coding assistant writes a full transcript to disk. Claude Code saves `.jsonl` files under `~/.claude/projects/`. Codex CLI writes to `~/.codex/sessions/`. Cursor, Gemini CLI, and Copilot each have their own stores.

These transcripts are rich. They contain:

- Every architectural decision you discussed with the AI
- Every debugging session, including the dead ends
- Every library you evaluated and why you picked one over another
- Code snippets you'll want again in six months

But the format is hostile. Raw JSONL. No search. No cross-referencing. No way to find "that time I debugged the WebSocket reconnection logic" without `grep`-ing through megabytes of JSON.

So you don't. The transcripts gather dust. Your accumulated knowledge evaporates.

## The solution: a local, searchable knowledge base

**llm-wiki** turns your dormant session history into a beautiful, searchable, interlinked knowledge base. Locally. In two commands. No cloud services. No API keys. No accounts.

```bash
git clone https://github.com/Pratiyush/llm-wiki.git
cd llm-wiki && ./setup.sh
./build.sh && ./serve.sh    # browse at http://127.0.0.1:8765
```

The tool follows [Andrej Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) -- a three-layer architecture where raw transcripts feed an LLM-maintained wiki that compiles into a static site.

## What you actually get

Go look at the [live demo](https://pratiyush.github.io/llm-wiki/) -- it rebuilds from synthetic sessions on every push, so it always shows the latest features. Here is what you will find:

**A home page with a 365-day activity heatmap.** Like GitHub's contribution graph, but for your AI coding sessions. At a glance, you can see when you leaned heavily on AI assistance and when you went solo.

![Home page with activity heatmap](docs/images/home.png)

**Every session, searchable and filterable.** A sortable table across all your projects. Filter by project, model, date range, or free text. Hit Cmd+K for a command palette with fuzzy search across everything.

![Sessions index with filter bar](docs/images/sessions.png)

**Session detail pages with syntax highlighting.** Every conversation rendered as clean, readable HTML with highlight.js-powered code blocks, collapsible tool results, breadcrumbs, and a reading progress bar.

![Session detail with code highlighting](docs/images/session-rust.png)

**An AI model directory.** Structured model profiles with context windows, pricing, benchmarks, and auto-generated side-by-side comparison pages. If you use multiple models, you can track how they compare over time with an append-only changelog and pricing sparklines.

**Multi-agent support.** Use Claude Code on Monday, Copilot on Tuesday, and Cursor on Wednesday? All three show up in the same wiki with colored agent badges so you can tell who wrote what.

**AI-consumable exports.** Every page ships as both HTML (for you) and machine-readable formats (`.txt`, `.json`, JSON-LD, `llms.txt`) so other AI agents can query your wiki directly. There is even an MCP server with 7 tools so Claude Desktop or Cursor can search your knowledge base live.

## The architecture

Three layers, per Karpathy's spec:

1. **Raw** (`raw/`) -- Immutable markdown converted from `.jsonl`. Redacted by default (usernames, API keys, tokens, emails). Never modified after conversion.

2. **Wiki** (`wiki/`) -- LLM-maintained pages. Sources, entities, concepts, syntheses, comparisons, all interlinked with `[[wikilinks]]`. Your coding agent builds this layer via slash commands like `/wiki-ingest`.

3. **Site** (`site/`) -- Static HTML you can browse locally or deploy to GitHub Pages / GitLab Pages / anywhere.

The build is deterministic and stdlib-only. The only runtime dependency is Python's `markdown` library. Syntax highlighting runs client-side via highlight.js from a CDN. No npm. No bundler. No database.

## Works with 6+ agents

| Agent | Status |
|---|---|
| Claude Code | Production since v0.1 |
| Codex CLI | Production since v0.3 |
| Copilot Chat + CLI | Production since v0.9 |
| Cursor | Production since v0.5 |
| Gemini CLI | Production since v0.5 |
| Obsidian | Bidirectional since v0.2 |
| PDF files | Production since v0.5 |

Adding a new agent is one small file -- subclass `BaseAdapter`, ship a fixture and a test.

## Privacy by default

Everything runs locally. Localhost-only binding. No telemetry. No cloud calls. Usernames, API keys, tokens, and emails are redacted before anything hits disk. A `.llmwikiignore` file (gitignore syntax) lets you skip entire projects or date ranges.

Your session history never leaves your machine unless you choose to deploy the site somewhere.

## What I learned from 337 sessions

Building this tool forced me to look at my own AI coding patterns. Some things I noticed:

- I ask the same architectural question in different ways across projects, and the AI gives different answers depending on context. The wiki surfaces these contradictions.
- My tool usage shifted dramatically over time. Early sessions were all Bash and Read. Later sessions leaned heavily on Edit and Grep. The tool-calling bar charts make this visible.
- The sessions I thought were throwaway debugging often contained the most reusable knowledge.

## Try it

The [live demo](https://pratiyush.github.io/llm-wiki/) shows every feature running against safe synthetic data. Your real wiki will look identical -- just with your actual work.

```bash
git clone https://github.com/Pratiyush/llm-wiki.git
cd llm-wiki && ./setup.sh
./build.sh && ./serve.sh
```

It takes about 5 minutes. No account needed. Works offline.

If you find it useful, [star the repo](https://github.com/Pratiyush/llm-wiki) and consider contributing -- the adapter pattern makes it straightforward to add support for new agents.

**Links:**
- GitHub: [github.com/Pratiyush/llm-wiki](https://github.com/Pratiyush/llm-wiki)
- Live demo: [pratiyush.github.io/llm-wiki](https://pratiyush.github.io/llm-wiki/)
- Karpathy's original spec: [gist.github.com/karpathy/442a6bf555914893e9891c11519de94f](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
