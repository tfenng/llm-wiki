# Playground

Try llmwiki locally with demo data. No agent sessions required.

## Live demo

Browse the live demo at [pratiyush.github.io/llm-wiki/](https://pratiyush.github.io/llm-wiki/). This is built from the demo sessions in `examples/demo-sessions/` and deployed via GitHub Pages.

## Running locally with demo data

```bash
# Clone and set up
git clone https://github.com/Pratiyush/llm-wiki.git
cd llm-wiki
./setup.sh

# Seed demo sessions
mkdir -p raw/sessions
cp -r examples/demo-sessions/* raw/sessions/

# Build and serve
python3 -m llmwiki build
python3 -m llmwiki serve --open
```

This opens [http://127.0.0.1:8765/](http://127.0.0.1:8765/) in your browser.

## Exploring the UI

### Command palette

Press **Cmd+K** (macOS) or **Ctrl+K** to open the command palette. Type to fuzzy-search across all projects, sessions, and pages. Press Enter to navigate.

### Search bar

Press **/** to focus the search bar. The search index covers session titles, project names, and content snippets. Results appear as you type.

### Keyboard shortcuts

Press **?** to see all available shortcuts:

| Key | Action |
|---|---|
| `Cmd+K` / `Ctrl+K` | Command palette |
| `/` | Focus search |
| `g h` | Go to home |
| `g p` | Go to projects |
| `g s` | Go to sessions |
| `j` / `k` | Navigate table rows (down / up) |
| `?` | Show shortcut help |

### Theme toggle

Click the theme toggle in the top-right corner to switch between light and dark mode. The site also respects your system preference via `prefers-color-scheme`.

### Session pages

Each session page includes:

- **Breadcrumbs** at the top (Home > Project > Session)
- **Reading progress bar** at the top of the viewport
- **YAML frontmatter** rendered as a metadata card (model, date, tools used, git branch)
- **Token usage card** with input/output/cache token breakdown
- **Tool-calling bar chart** showing which tools were used and how often
- **Collapsible tool-result sections** for long outputs (click to expand)
- **Copy buttons** on code blocks (copies to clipboard)
- **Copy-as-markdown** button to copy the entire session

### Project pages

Each project page shows:

- **Topic chips** -- auto-detected subject tags
- **Session list** with date, model, and agent badge
- **Token usage summary** across all sessions
- **Tool usage chart** aggregated across sessions

### Home page

The home page includes:

- **365-day activity heatmap** (GitHub-style) showing session frequency
- **Site stats** (total sessions, projects, tokens)
- **Recently updated** list
- **Project directory** with session counts

### Models page

Navigate to `/models/` to see structured profile pages for every LLM model referenced in your sessions, including pricing and context window information.

### Comparisons page

Navigate to `/comparisons/` to see auto-generated side-by-side diffs of related entities and concepts.

## Trying the wiki layer

To try the LLM-maintained wiki (Karpathy layer 2), you need an active Claude Code session:

```bash
# Inside a Claude Code session at the repo root:
/wiki-ingest raw/sessions/
```

This reads the demo sessions, writes summary pages to `wiki/`, and cross-links entities. Then rebuild:

```bash
python3 -m llmwiki build
python3 -m llmwiki serve --open
```

The wiki content will appear alongside the session pages.

## Trying exports

```bash
# Generate all AI-consumable formats
python3 -m llmwiki export all

# Build the knowledge graph
python3 -m llmwiki graph

# Check for broken links
python3 -m llmwiki check-links

# Run structural eval
python3 -m llmwiki eval --json
```
