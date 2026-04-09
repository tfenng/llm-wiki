# Show HN Post Draft

**Target:** Hacker News (Show HN)
**Tone:** Concise, technical, no marketing speak

---

## Title

Show HN: llm-wiki -- Turn your AI coding sessions into a searchable wiki

## Body

Every AI coding assistant (Claude Code, Copilot, Cursor, Codex CLI, Gemini CLI) writes full session transcripts to disk. Most developers have hundreds of them and never look at them again.

llm-wiki converts them into a searchable, interlinked knowledge base following Karpathy's three-layer LLM Wiki architecture [1]:

1. Raw layer: JSONL -> redacted markdown with rich frontmatter
2. Wiki layer: LLM-maintained entity/concept/source pages with [[wikilinks]]
3. Site layer: static HTML with Cmd+K search, syntax highlighting, dark mode

What I think is interesting about the implementation:

- Supports 6 AI agents via a pluggable adapter pattern (one ~50-line file per agent)
- All visualizations (365-day heatmap, tool charts, token usage, pricing sparklines) are pure SVG generated at build time -- no JS charting library
- Every page ships in three formats: HTML for humans, .txt and .json for AI agents. Plus llms.txt, JSON-LD, and an MCP server with 7 tools.
- Stdlib-only Python. The single runtime dep is the `markdown` library. No npm, no database, no template engine. HTML is generated with f-strings in one file.
- 472 tests including a Playwright E2E suite with 62 Gherkin scenarios

The live demo rebuilds from synthetic sessions on every push: https://pratiyush.github.io/llm-wiki/

GitHub: https://github.com/Pratiyush/llm-wiki

Setup is three commands: `git clone`, `./setup.sh`, `./build.sh && ./serve.sh`

Python 3.9+. MIT license. Works offline. No API key.

[1] https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

---

## Notes for submitter

- Post between 8-10 AM ET on a weekday (Tuesday-Thursday tend to work best)
- Do not editorialize the title -- "Show HN: <name> -- <one line>" is the standard format
- Be ready to answer comments promptly for the first 2 hours
- Common HN questions to prepare for:
  - "Why not just use grep?" -- Answer: cross-referencing, visualization, multi-agent unification, wiki layer
  - "Why not Obsidian?" -- Answer: Obsidian is supported as an input source; llm-wiki adds the session-transcript pipeline and static site
  - "Why stdlib-only?" -- Answer: Every dep is maintenance burden + security surface + contribution barrier
  - "Does this require an LLM to use?" -- Answer: Layer 1 (raw) and layer 3 (site) work without an LLM. Layer 2 (wiki) benefits from one but is optional.
  - "Privacy?" -- Answer: Everything local, auto-redaction, .llmwikiignore, localhost-only, no telemetry
