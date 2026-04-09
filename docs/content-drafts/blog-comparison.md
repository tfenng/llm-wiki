# llm-wiki vs mem0 vs Rewind vs Manual Notes

**Target:** Dev blog, comparison/review sites
**Length:** ~1,200 words
**Tone:** Neutral, practical comparison

---

If you use AI coding assistants daily, your accumulated session knowledge is one of your most underutilized assets. Several tools try to solve this in different ways. This post compares four approaches: [llm-wiki](https://github.com/Pratiyush/llm-wiki) (local, open-source), [mem0](https://mem0.ai) (cloud memory layer), [Rewind](https://www.rewind.ai/) (screen recording), and plain manual notes.

## Comparison table

| | llm-wiki | mem0 | Rewind | Manual notes |
|---|---|---|---|---|
| **Type** | Local static-site generator | Cloud memory API | Screen recording + search | Markdown/Notion/Obsidian |
| **Data source** | Agent JSONL transcripts | API calls / app integrations | Screen + audio capture | What you remember to write |
| **Storage** | Local filesystem | Cloud (mem0 servers) | Local + cloud | Wherever you put them |
| **Cost** | Free (MIT license) | Free tier + paid plans | $24.99/month | Free |
| **Privacy** | Everything local, redacted by default | Data sent to mem0 cloud | Records everything on screen | You control it |
| **Offline** | Yes, fully | No (cloud API) | Partially (local recording) | Yes |
| **API key required** | No | Yes | No | No |
| **AI agents supported** | Claude Code, Codex CLI, Copilot, Cursor, Gemini CLI, Obsidian, PDF | Any (via API) | Any (screen-level) | N/A |
| **Search** | Cmd+K fuzzy search + MCP | Semantic search via API | Natural language search | Depends on tool |
| **Cross-referencing** | Wikilinks, entity/concept pages, auto-comparisons | Memory associations | Timeline correlation | Manual linking |
| **Visualization** | Activity heatmap, tool charts, token usage, pricing sparklines | Dashboard (paid) | Timeline view | None |
| **Output format** | Static HTML + AI exports (llms.txt, JSON-LD, per-page .txt/.json) | API responses | Proprietary app | Markdown |
| **Deployment** | GitHub Pages, GitLab Pages, any static host | N/A (SaaS) | N/A (desktop app) | Git, Notion, etc. |
| **Setup time** | ~5 minutes | ~15 minutes (API integration) | ~5 minutes (install app) | Ongoing |
| **Open source** | Yes (MIT) | Partially (SDK open, server closed) | No | N/A |

## When to use each

### Use llm-wiki when:

- You want a **permanent, searchable archive** of your AI coding sessions
- Privacy matters -- nothing leaves your machine unless you deploy it
- You use **multiple AI assistants** and want them unified in one place
- You want **structured data** -- not just text search, but entity pages, concept pages, cross-links, model comparisons, and trend visualizations
- You are comfortable with a CLI workflow (`sync`, `build`, `serve`)
- You want machine-readable exports for other AI agents (MCP server, llms.txt, JSON-LD)

### Use mem0 when:

- You need **real-time memory** that persists across API calls (e.g., building a chatbot that remembers users)
- You are building an **application** that needs a memory layer, not archiving personal sessions
- You want **semantic search** over memories without running your own embedding pipeline
- You are fine sending data to a cloud service

### Use Rewind when:

- You want to capture **everything on your screen**, not just AI coding sessions
- You need to search across meetings, browser tabs, documents, and conversations
- You prefer a **zero-effort** passive capture approach
- You are on macOS and willing to pay $24.99/month

### Use manual notes when:

- Your volume is low (a few sessions per week)
- You have a strong existing note-taking habit
- You want full control over what gets recorded and how
- You do not need automated cross-referencing or visualizations

## llm-wiki's unique strengths

**Multi-agent unification.** If you use Claude Code for backend work, Copilot for frontend, and Cursor for quick fixes, llm-wiki puts all three in the same searchable wiki with colored agent badges. No other tool does this at the transcript level.

**Karpathy-standard architecture.** The three-layer model (raw, wiki, site) is not arbitrary. It follows a [well-reasoned spec](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) that separates immutable sources from generated knowledge from rendered output. This means you can regenerate the wiki without losing raw data, and rebuild the site without losing wiki content.

**Works offline, permanently.** There is no server to shut down, no subscription to lapse, no API to deprecate. The output is static HTML files. You could put them on a USB drive and read them in 10 years.

**AI-consumable by design.** Every page ships as HTML, plain text, and structured JSON. There is an MCP server so AI agents can query your wiki. There is a JSON-LD knowledge graph. There is an llms.txt file per the llmstxt.org spec. Your wiki is not just for human eyes.

**Pure-SVG visualizations.** The activity heatmap, tool-calling charts, token usage cards, and pricing sparklines are all rendered as SVG at build time. No JavaScript charting library. They work in RSS readers, print cleanly, and load instantly.

**No cost, no vendor lock-in.** MIT license. Python stdlib + `markdown`. Deploy to GitHub Pages for free. Export to Obsidian, qmd, or any other format. Your data stays yours.

## Where llm-wiki falls short

To be fair about the trade-offs:

- **Requires a build step.** You run `sync` and `build` commands. It is not automatic capture like Rewind.
- **No semantic search.** The built-in search is keyword-based fuzzy matching. For semantic search, you would pipe the exports through an embedding pipeline (the qmd exporter is designed for this).
- **CLI-first.** There is no GUI for configuration. You edit a JSON config file and run shell commands.
- **Wiki layer needs an LLM.** The raw-to-wiki synthesis (layer 2) works best when driven by Claude Code or similar. Without it, you still get a browsable session archive, but not the structured knowledge graph.

## Verdict

These tools solve different problems, and they are not mutually exclusive. You could use Rewind for passive screen capture, mem0 for your chatbot's memory, manual notes for high-level project journals, and llm-wiki for your AI coding session archive.

If your primary goal is turning your AI coding history into something you will actually use again, llm-wiki is the most complete solution available -- and it costs nothing.

**Links:**
- llm-wiki: [github.com/Pratiyush/llm-wiki](https://github.com/Pratiyush/llm-wiki)
- Live demo: [pratiyush.github.io/llm-wiki](https://pratiyush.github.io/llm-wiki/)
- mem0: [mem0.ai](https://mem0.ai)
- Rewind: [rewind.ai](https://www.rewind.ai/)
