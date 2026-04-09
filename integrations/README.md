# llm-wiki Integrations

Scaffold implementations showing how llm-wiki connects to other tools. Each integration is minimal but functional enough to demonstrate the pattern.

## Directory

| Integration | Type | Status | Description |
|---|---|---|---|
| [vscode/](vscode/) | VS Code extension | Scaffold | Sidebar tree view, sync/build commands, open site in browser |
| [obsidian/](obsidian/) | Obsidian plugin | Scaffold | Sync wiki/ into an Obsidian vault, preserving native `[[wikilinks]]` |
| [raycast/](raycast/) | Raycast extension | Scaffold | Full-text search across wiki pages from Raycast |
| [alfred/](alfred/) | Alfred workflow | Scaffold | Script Filter search via `wiki <query>` keyword |
| [webhook/](webhook/) | GitHub webhook | Scaffold | Auto-sync on push via stdlib HTTP handler |

## In-package Exporters

These live in the `llmwiki/` package rather than `integrations/`:

| Module | Status | Description |
|---|---|---|
| `llmwiki.export_jupyter` | Scaffold | Export wiki sections as Jupyter notebooks (.ipynb) |
| `llmwiki.export_marp` | Shipped | Export wiki pages as Marp slide decks |
| `llmwiki.export_qmd` | Shipped | Export for qmd hybrid search |
| `llmwiki.obsidian_output` | Shipped | Full Obsidian vault export (`export-obsidian` CLI) |

## Contributing

Each integration should:

1. Be self-contained in its directory with its own README
2. Use the llmwiki CLI (`python3 -m llmwiki <subcommand>`) as the interface — do not import llmwiki internals
3. Provide enough scaffolding to build and test locally
4. Stay stdlib-only for Python integrations; minimize dependencies for JS/TS integrations

To promote a scaffold to "shipped" status:

1. Add end-to-end tests
2. Wire up any needed CLI subcommands in `llmwiki/cli.py`
3. Update this table
4. Add a changelog entry
