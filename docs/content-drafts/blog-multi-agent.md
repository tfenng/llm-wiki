# Multi-Agent Development: Claude + Codex + Copilot in One Wiki

**Target:** Dev blog, AI tooling audience
**Length:** ~1,200 words
**Tone:** Practical, opinionated

---

Most developers using AI coding assistants do not use just one. They use three or more.

Claude Code for complex refactoring. Copilot for inline completions. Cursor for quick prototyping. Codex CLI for batch operations. Gemini CLI for exploring alternatives. Maybe Obsidian for notes that tie it all together.

Each tool writes session data to a different location, in a different format, with different metadata. The result is that your AI-assisted development knowledge is fragmented across five stores that never talk to each other.

[llm-wiki](https://github.com/Pratiyush/llm-wiki) unifies them.

## The multi-agent reality

A typical week for a developer using AI assistants in 2026 might look like this:

- **Monday:** Claude Code session to scaffold a new microservice, 45 minutes of architecture discussion, model choice, API design
- **Tuesday:** Copilot Chat to debug a failing test, 15 minutes of back-and-forth
- **Wednesday:** Cursor to prototype a UI component, rapid iteration with inline suggestions
- **Thursday:** Codex CLI to batch-rename 200 files across a monorepo
- **Friday:** Gemini CLI to get a second opinion on a performance optimization approach

By Friday, you have five valuable conversations scattered across five different tools. You will never look at any of them again -- unless you have a system that aggregates them.

## How llm-wiki unifies session histories

The tool uses an **adapter pattern** to normalize different agent formats into a common structure. Each agent gets a thin adapter (typically 50-100 lines of Python) that knows:

1. Where the agent stores its session data on your filesystem
2. How to discover and iterate over session files
3. How to derive a project name from the file path

Everything else -- JSONL parsing, record filtering, redaction, markdown rendering, frontmatter generation -- is shared infrastructure in the core converter.

Currently shipping adapters:

| Agent | Store location | Status |
|---|---|---|
| Claude Code | `~/.claude/projects/*/*.jsonl` | Production (v0.1) |
| Codex CLI | `~/.codex/sessions/**/*.jsonl` | Production (v0.3) |
| Copilot Chat | VS Code workspace storage | Production (v0.9) |
| Copilot CLI | `~/.config/github-copilot/` | Production (v0.9) |
| Cursor | Cursor workspace storage | Production (v0.5) |
| Gemini CLI | `~/.gemini/` | Production (v0.5) |
| Obsidian | Configurable vault paths | Production (v0.1) |
| PDF | Configurable paths | Production (v0.5) |

When you run `llmwiki sync`, every enabled adapter scans its store, and all discovered sessions flow into the same `raw/sessions/` directory. The build step renders them into one unified site.

## Agent labels: who said what

Starting in v0.9, every session page and table row carries a **colored agent badge** so you can tell at a glance which AI wrote what:

- **Claude Code** -- purple badge
- **Codex CLI** -- green badge
- **Copilot** -- dark badge
- **Cursor** -- blue badge
- **Gemini CLI** -- teal badge

On project pages that aggregate sessions from multiple agents, the badges make the mix immediately visible. You can see that your `api-gateway` project had 12 Claude Code sessions, 3 Copilot sessions, and 1 Gemini CLI session.

The sessions index table supports filtering by agent, so you can pull up "every Codex CLI session from the last month" in two clicks.

## Use case: comparing approaches across agents

This is where multi-agent wikis get genuinely useful.

Suppose you asked Claude Code and Gemini CLI the same question: "How should I structure the authentication middleware for this Express app?" You will get different answers. Maybe Claude suggests a middleware chain pattern. Maybe Gemini suggests a decorator approach.

Without llm-wiki, those two answers live in separate tools and you forget the comparison existed. With llm-wiki, both sessions appear in the same project, searchable from the same command palette. The wiki layer (Karpathy layer 2) can even create a comparison page that surfaces the differences explicitly.

Some patterns that emerge from multi-agent wikis:

- **Model strength mapping.** Over time, you notice which agent gives better answers for which tasks. Claude Code might be consistently better at large refactors; Copilot might be faster for small fixes. The tool-calling bar charts and session metadata make this visible.
- **Cost comparison.** Token usage cards show exactly how many tokens each agent consumed. If you are paying for multiple services, this data tells you where your money goes.
- **Approach diversity.** Different models trained on different data suggest different solutions. Seeing them side by side in one wiki is like having a panel of consultants instead of one.

## The structured model directory

llm-wiki's `/models/` section gives you a directory of every AI model you have used, with structured profiles: provider, context window, pricing, benchmarks, and modalities. The build pipeline auto-generates **vs-comparison pages** between model pairs that share enough data points, producing side-by-side tables with difference highlighting and benchmark bar charts.

Combined with the **append-only changelog** on each model entity, you can track how models evolve over time -- price cuts, context window expansions, benchmark improvements -- all with timestamps and source links.

## Adding a new agent

If your favorite agent is not supported yet, the adapter pattern makes it straightforward to add one. The contract:

1. Create `llmwiki/adapters/<agent>.py`
2. Subclass `BaseAdapter`
3. Implement `session_store_path()`, `discover_sessions()`, and `project_slug()`
4. Add a synthetic fixture at `tests/fixtures/<agent>/minimal.jsonl`
5. Add a snapshot test
6. Add a doc page at `docs/adapters/<agent>.md`

The Copilot adapter (supporting both Chat and CLI variants) was shipped in a single PR. Most adapters are under 100 lines.

## Try it

If you use two or more AI coding assistants, the multi-agent view alone is worth the 5-minute setup:

```bash
git clone https://github.com/Pratiyush/llm-wiki.git
cd llm-wiki && ./setup.sh
./sync.sh && ./build.sh && ./serve.sh
```

The [live demo](https://pratiyush.github.io/llm-wiki/) shows three synthetic projects to give you a feel for the UI, but the real value appears when you run it on your own sessions and see months of fragmented AI interactions unified in one place.

**Links:**
- GitHub: [github.com/Pratiyush/llm-wiki](https://github.com/Pratiyush/llm-wiki)
- Live demo: [pratiyush.github.io/llm-wiki](https://pratiyush.github.io/llm-wiki/)
- Adapter docs: [github.com/Pratiyush/llm-wiki/tree/master/docs/adapters](https://github.com/Pratiyush/llm-wiki/tree/master/docs/adapters)
