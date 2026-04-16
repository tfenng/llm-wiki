# Set Up llm-wiki in 5 Minutes

**Target:** Dev blog, getting-started tutorial
**Length:** ~1,000 words
**Tone:** Step-by-step, friendly, practical

---

You have hundreds of AI coding session transcripts on your hard drive. Let's turn them into a searchable knowledge base in under 5 minutes.

By the end of this tutorial, you will have a local website with every Claude Code, Codex CLI, Copilot, Cursor, or Gemini CLI session you have ever run -- searchable, cross-referenced, and syntax-highlighted.

## Prerequisites

- **Python 3.9+** (macOS ships with it; most Linux distros do too)
- **Git**
- At least a few AI coding sessions already on disk (Claude Code, Codex CLI, Copilot, Cursor, or Gemini CLI)

That's it. No npm. No Docker. No database. No account.

## Step 1: Clone and install

### macOS / Linux

```bash
git clone https://github.com/Pratiyush/llm-wiki.git
cd llm-wiki
./setup.sh
```

### Windows

```cmd
git clone https://github.com/Pratiyush/llm-wiki.git
cd llm-wiki
setup.bat
```

The setup script installs the `markdown` library (the only runtime dependency), scaffolds the data directories (`raw/`, `wiki/`, `site/`), detects which AI agents you have installed, and runs a dry-run sync to show what it found.

![Screenshot: setup.sh output showing detected agents](docs/images/home.png)

You should see output listing your detected adapters (e.g., "Claude Code: found 42 sessions" or "Codex CLI: found 15 sessions").

## Step 2: Sync your sessions

```bash
./sync.sh
```

This converts every discovered `.jsonl` transcript into clean, redacted markdown under `raw/sessions/<project>/`. Each file gets rich frontmatter (project name, model used, tools called, token counts, duration).

**Privacy note:** Usernames, API keys, tokens, and emails are redacted automatically before anything hits disk. You can add custom patterns and exclusions in `config.json` or `.llmwikiignore`.

## Step 3: Build the site

```bash
./build.sh
```

This compiles everything into a static HTML site under `site/`. The build is fast (typically under 5 seconds for hundreds of sessions) and produces:

- A home page with activity heatmap and project grid
- Per-project pages with tool charts and token timelines
- Per-session pages with the full conversation and syntax highlighting
- A command palette (Cmd+K) with fuzzy search across everything
- AI-consumable exports (llms.txt, JSON-LD, per-page .txt/.json siblings)

## Step 4: Browse your wiki

```bash
./serve.sh
```

Open [http://127.0.0.1:8765/](http://127.0.0.1:8765/) in your browser.

![Screenshot: llm-wiki home page](docs/images/home.png)

Try these keyboard shortcuts:

| Shortcut | Action |
|---|---|
| `Cmd+K` or `Ctrl+K` | Open the command palette |
| `/` | Focus the search bar |
| `g h` | Go to home |
| `g p` | Go to projects |
| `g s` | Go to sessions |
| `j` / `k` | Navigate table rows |
| `?` | Show all shortcuts |

## Step 5 (optional): Build the wiki layer

The steps above give you a browsable session archive. To build the full Karpathy-style wiki -- with entity pages, concept pages, cross-references, and syntheses -- you need an LLM in the loop.

Inside a Claude Code session at the repo root:

```
/wiki-ingest raw/sessions/<your-project>/
```

The agent reads your session transcripts, writes summary pages, creates entity and concept pages, and cross-links everything with `[[wikilinks]]`. Then rebuild:

```bash
./build.sh
```

## Step 6 (optional): Set up auto-sync

To sync automatically every time you start Claude Code, add a `SessionStart` hook to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "(python3 /absolute/path/to/llm-wiki/llmwiki/convert.py > /tmp/llmwiki-sync.log 2>&1 &) ; exit 0"
          }
        ]
      }
    ]
  }
}
```

For daily scheduled syncs (without Claude Code), run `llmwiki schedule` to auto-generate the task file for your OS, or copy a reference template from `examples/scheduled-sync-templates/` (macOS launchd, Linux systemd, Windows Task Scheduler).

## Step 7 (optional): Deploy to GitHub Pages

The repo includes a GitHub Actions workflow that builds and deploys your site automatically:

1. Push the repo to GitHub
2. Enable GitHub Pages in Settings > Pages (source: GitHub Actions)
3. Push to master

Your wiki will be live at `https://<username>.github.io/llm-wiki/`. A GitLab Pages workflow is also available.

## Troubleshooting

**"No sessions found"**

Make sure you have at least one completed AI coding session. Check that your agent's session store exists:
- Claude Code: `~/.claude/projects/`
- Codex CLI: `~/.codex/sessions/`
- Cursor: `~/Library/Application Support/Cursor/User/workspaceStorage/` (macOS)
- Gemini CLI: `~/.gemini/`

Run `llmwiki adapters` to see which agents are detected.

**"Build produces empty site"**

Run `./sync.sh` first. The build reads from `raw/sessions/`, which sync populates.

**"Syntax highlighting not working"**

highlight.js loads from a CDN at view time. If you are fully offline, code blocks will render as plain monospace text but still be readable.

**"Want to exclude certain projects"**

Create a `.llmwikiignore` file at the repo root (gitignore syntax):

```
# Skip a whole project
confidential-client/
# Skip anything before a date
*2025-*
```

## Next steps

- Browse the [live demo](https://pratiyush.github.io/llm-wiki/) to see every feature
- Read the [architecture docs](https://github.com/Pratiyush/llm-wiki/blob/master/docs/architecture.md) to understand the three-layer design
- [Star the repo](https://github.com/Pratiyush/llm-wiki) if you find it useful

**Links:**
- GitHub: [github.com/Pratiyush/llm-wiki](https://github.com/Pratiyush/llm-wiki)
- Live demo: [pratiyush.github.io/llm-wiki](https://pratiyush.github.io/llm-wiki/)
