# Awesome List Submission Drafts

Draft PR descriptions for submitting llmwiki to curated awesome lists.
Copy-paste and adapt as needed.

---

## awesome-python

**Repository:** [vinta/awesome-python](https://github.com/vinta/awesome-python)

**Category:** Documentation / Text Processing

**Suggested placement:** Under "Documentation" or "Text Processing > Markdown"

**One-line description:**

```
- [llmwiki](https://github.com/Pratiyush/llm-wiki) - Turn Claude Code, Codex CLI, Cursor, Copilot, and Gemini CLI session transcripts into a searchable, interlinked knowledge base with a static HTML site. Stdlib-only, no API keys needed.
```

**PR title:** Add llmwiki to Documentation

**PR body:**

llmwiki converts `.jsonl` session transcripts from AI coding agents
(Claude Code, Codex CLI, Cursor, GitHub Copilot, Gemini CLI) into a
Karpathy-style knowledge wiki with a beautiful static HTML site.

Why it belongs here:
- Pure Python (3.9+), stdlib-only core (no numpy, no torch, no API keys)
- pip-installable via PyPI
- Covers a use case no other tool does: structured knowledge extraction
  from AI coding sessions
- 472 tests, WCAG 2.1 AA accessible, MIT licensed

Live demo: https://pratiyush.github.io/llm-wiki/

---

## awesome-llm-tools

**Repository:** Search for the most active awesome-llm or awesome-llm-tools list on GitHub (several exist; pick the one with the most stars and recent activity).

**Category:** Knowledge Management / Session History

**Suggested placement:** Under "Knowledge Management", "Developer Tools", or "Session Management"

**One-line description:**

```
- [llmwiki](https://github.com/Pratiyush/llm-wiki) - Local-first knowledge base that compiles Claude Code, Codex, Cursor, Copilot, and Gemini CLI sessions into an interlinked wiki + static site. Based on Karpathy's LLM Wiki spec.
```

**PR title:** Add llmwiki -- LLM session history to knowledge wiki

**PR body:**

llmwiki is the missing tool for anyone who uses AI coding agents daily
but never looks at their session history again.

It converts raw `.jsonl` transcripts into:
- Clean, redacted markdown with YAML frontmatter
- A Karpathy-style wiki (sources, entities, concepts, syntheses)
- A static HTML site with dark mode, global search, activity heatmap,
  and token usage analytics

Key differentiators:
- Multi-agent: Claude Code + Codex CLI + Cursor + Copilot + Gemini CLI
- Local-first: runs entirely on your machine, no cloud, no API keys
- AI-consumable: ships `llms.txt`, JSON-LD, per-page `.txt`/`.json`,
  and an MCP server
- Stdlib-only Python (no numpy, no torch, no node)

Live demo: https://pratiyush.github.io/llm-wiki/

---

## awesome-static-site-generators

**Repository:** [myles/awesome-static-generators](https://github.com/myles/awesome-static-generators)

**Category:** Python / Documentation

**Suggested placement:** Under "Python" (the list is organized by language)

**One-line description:**

```
- [llmwiki](https://github.com/Pratiyush/llm-wiki) - Generates a static knowledge-base site from AI coding agent session transcripts. Dark mode, global search, activity heatmaps, syntax highlighting. Python, stdlib-only.
```

**PR title:** Add llmwiki (AI session history to static site)

**PR body:**

llmwiki is a static site generator for a specific domain: AI coding
agent session transcripts (Claude Code, Codex CLI, Cursor, Copilot,
Gemini CLI).

It reads `.jsonl` session files, converts them to markdown, and builds
a fully-featured static site with:
- Dark mode + system-aware theme toggle
- Cmd+K command palette with fuzzy search
- highlight.js syntax highlighting
- 365-day activity heatmap
- Tool-usage and token-usage visualizations
- WCAG 2.1 AA accessible
- AI-consumable exports (llms.txt, JSON-LD, sitemap, RSS)

Python 3.9+, stdlib-only (no npm, no bundler, no database). Two
commands to go from raw transcripts to deployed site.

Live demo: https://pratiyush.github.io/llm-wiki/

---

## Submission checklist

Before submitting to any awesome list:

- [ ] Verify the list's contributing guidelines (most require the
      project to be "awesome", not just functional)
- [ ] Check that llmwiki is not already listed
- [ ] Confirm the suggested category still exists in the current README
- [ ] Match the list's formatting conventions (some use `-`, some `*`,
      some require descriptions, some don't)
- [ ] Include the live demo link -- it's the strongest argument
- [ ] Wait for at least 50 GitHub stars before submitting (many lists
      have minimum thresholds)
