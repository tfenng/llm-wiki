---
title: "Agent mode"
type: navigation
docs_shell: true
---

<div style="background: #0D9488; color: white; padding: 8px 16px; border-radius: 6px; font-weight: 600; margin-bottom: 24px;">AGENT MODE — uses your existing Claude Code / Codex CLI session.</div>

# Mode B · Agent

Runs synthesis + query **inside** the Claude Code or Codex CLI session
that's already open on your machine — no separate API key, no
incremental cost beyond your existing agent subscription.

## Status

Ships today for every command that's already a prompt-driven
workflow: `/wiki-sync`, `/wiki-ingest`, `/wiki-query`, `/wiki-reflect`,
`/wiki-update`, `/wiki-lint`.  A dedicated `agent-delegate` backend
that lets `llmwiki synthesize` marshal prompts back to the running
agent is tracked under **[#316 · feat: Mode B agent-delegate synthesis](https://github.com/Pratiyush/llm-wiki/issues/316)**.

Until #316 merges, `synthesize` uses one of the local backends
(`dummy` / `ollama`) even in Agent mode — but every **other** slash
command works end-to-end.

## Setup (no API key)

Just install the slash commands:

```bash
llmwiki install-skills   # copies .claude/commands/*.md into ~/.claude/
```

That's it.  Open Claude Code, type `/wiki-sync`, and it runs.

## Daily flow

```
You: /wiki-sync
Claude: (runs python3 -m llmwiki sync, ingests new pages)

You: /wiki-query when did I last change the convert pipeline?
Claude: (reads wiki/index.md + the relevant source pages, synthesizes)

You: /wiki-graph
Claude: (writes graph/ + opens site/graph.html in your browser)
```

## When to pick this mode

- You already pay for Claude Code or Codex CLI — no extra bill.
- Exploratory work where you want the model to narrate what it's
  doing ("I'm now reading wiki/sources/...").
- Small-to-medium corpus (< 50 sessions) — serial synthesis isn't a
  bottleneck.
- Local-only privacy — no session content leaves your laptop except
  through the agent's existing plumbing.

## Limitations vs Mode A

- **Serial only** — one turn at a time, no batch.  A 647-session
  sync takes hours.
- **Needs the agent to be running** — can't schedule via cron.
- **Subject to the agent's context window** — long synthesize runs
  get truncated.

## See also

- [API mode](../api/) — pay per token to unlock batch + headless.
- [Slash commands reference](../../reference/slash-commands.md) — every
  `/wiki-*` command in one list.
- [Cheatsheet](../../cheatsheet.md) — daily-flow commands on one page.
