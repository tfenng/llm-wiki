# LinkedIn Launch Announcement

**Target:** LinkedIn
**Length:** ~280 words
**Tone:** Professional, enthusiastic without hype

---

I just open-sourced llm-wiki -- a tool that turns your AI coding session transcripts into a searchable, interlinked knowledge base.

If you use Claude Code, Copilot, Cursor, Codex CLI, or Gemini CLI, you already have hundreds of session transcripts sitting on your hard drive. Full conversations about architecture decisions, debugging sessions, code reviews. Write-once, read-never.

llm-wiki changes that. It follows Andrej Karpathy's LLM Wiki architecture (three layers: raw sources, LLM-maintained wiki, generated static site) to convert dormant JSONL transcripts into a beautiful, browsable website you can run locally or deploy to GitHub Pages.

What it does:

- Supports 6 AI agents (Claude Code, Codex CLI, Copilot, Cursor, Gemini CLI, Obsidian) with a pluggable adapter pattern
- Renders a full static site with Cmd+K search, dark mode, syntax highlighting, keyboard shortcuts, and mobile support
- Generates activity heatmaps, tool-calling charts, token usage visualizations, and AI model comparison pages -- all as pure SVG at build time
- Ships machine-readable exports (llms.txt, JSON-LD, per-page .txt/.json) so other AI agents can query your wiki
- Includes an MCP server with 7 tools for live querying from Claude Desktop or Cursor
- Runs entirely local. No cloud. No API key. No telemetry. Privacy by default with automatic redaction.

The whole thing is Python stdlib + markdown. No npm. No database. MIT license.

Live demo (built from synthetic sessions, no personal data): https://pratiyush.github.io/llm-wiki/

GitHub: https://github.com/Pratiyush/llm-wiki

Based on Karpathy's spec: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

If you work with AI coding assistants daily, give it a try. Setup takes about 5 minutes. Stars and contributions welcome.

#OpenSource #AI #DeveloperTools #Python #ClaudeCode #CodingAssistant #KnowledgeBase
