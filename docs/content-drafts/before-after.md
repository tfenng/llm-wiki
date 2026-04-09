# Before / After: Raw JSONL to Wiki Site

This page shows the transformation pipeline from raw session data to
finished output. Use it in blog posts, talks, or the README to
communicate what llmwiki does at a glance.

## Before: raw `.jsonl` transcript

This is what Claude Code writes to disk after every session. One JSON
object per line, hundreds of lines per session, across hundreds of
files.

```jsonl
{"type":"summary","summary":"Set up Rust blog engine with Actix-web, Tera templates, and pulldown-cmark.","model":"claude-sonnet-4-20250514","totalCost":0.12}
{"parentMessageId":"root","role":"user","message":{"content":"I want to build a static blog engine in Rust. Let's start with the project scaffold."},"timestamp":"2026-04-01T14:22:03Z"}
{"parentMessageId":"msg_001","role":"assistant","message":{"content":"I'll scaffold a Rust blog engine for you. Let me start by creating the project structure with cargo."},"timestamp":"2026-04-01T14:22:08Z"}
{"parentMessageId":"msg_002","role":"tool","toolName":"Bash","input":{"command":"cargo init --name blog-engine"},"output":"Created binary (application) `blog-engine` package","timestamp":"2026-04-01T14:22:12Z"}
{"parentMessageId":"msg_003","role":"assistant","message":{"content":"Project created. Now let me set up the dependencies in Cargo.toml."},"timestamp":"2026-04-01T14:22:15Z"}
{"parentMessageId":"msg_004","role":"tool","toolName":"Write","input":{"file_path":"Cargo.toml","content":"[package]\nname = \"blog-engine\"\nversion = \"0.1.0\"\nedition = \"2021\"\n\n[dependencies]\nactix-web = \"4\"\ntera = \"1\"\npulldown-cmark = \"0.10\"\n"},"timestamp":"2026-04-01T14:22:20Z"}
{"parentMessageId":"msg_005","role":"assistant","message":{"content":"Dependencies added. Let me create the main entry point with Actix-web routing."},"timestamp":"2026-04-01T14:22:25Z"}
{"parentMessageId":"msg_006","role":"tool","toolName":"Write","input":{"file_path":"src/main.rs","content":"use actix_web::{web, App, HttpServer, HttpResponse};\n\n#[actix_web::main]\nasync fn main() -> std::io::Result<()> {\n    HttpServer::new(|| App::new().route(\"/\", web::get().to(index)))\n        .bind(\"127.0.0.1:8080\")?\n        .run().await\n}"},"timestamp":"2026-04-01T14:22:30Z"}
{"parentMessageId":"msg_007","role":"user","message":{"content":"Great, now add the markdown rendering pipeline."},"timestamp":"2026-04-01T14:23:45Z"}
{"parentMessageId":"msg_008","role":"assistant","message":{"content":"I'll add a markdown-to-HTML pipeline using pulldown-cmark with syntax highlighting support."},"timestamp":"2026-04-01T14:23:50Z"}
```

**Problems:**
- Unreadable without tooling
- No cross-referencing between sessions
- No search
- No way to see patterns across weeks of work
- Sitting dormant in `~/.claude/projects/` forever

## After: converted markdown (intermediate)

The converter transforms each session into clean, frontmatter'd markdown:

```markdown
---
title: "Rust blog engine scaffold"
slug: 2026-04-01-rust-blog-scaffold
project: demo-blog-engine
model: claude-sonnet-4-20250514
started: 2026-04-01T14:22:03Z
duration_seconds: 387
messages: 24
tools_used: [Bash, Write, Read, Grep]
tool_counts: {"Bash": 8, "Write": 12, "Read": 3, "Grep": 1}
tags: [rust, actix-web, tera, pulldown-cmark, blog, ssg]
---

# Rust blog engine scaffold

## Summary

Scaffolded a Rust static blog engine using Actix-web for the HTTP
server, Tera for HTML templates, and pulldown-cmark for Markdown
rendering. Created the project structure, configured dependencies,
and implemented the core rendering pipeline.

## Conversation

**User:** I want to build a static blog engine in Rust...

**Assistant:** I'll scaffold a Rust blog engine for you...

> **Bash** `cargo init --name blog-engine`
> Created binary (application) `blog-engine` package

**Assistant:** Project created. Now let me set up the dependencies...
```

**Improvements over raw JSONL:**
- Human-readable prose with structured metadata
- Frontmatter enables filtering, sorting, and aggregation
- Tool output collapsed and summarized
- PII redacted (usernames, API keys, tokens, emails)

## After: the HTML site (final output)

The builder turns every markdown file into a page on a beautiful static
site:

- **Session page** — full conversation with syntax-highlighted code
  blocks, collapsible tool results, breadcrumbs, reading time estimate,
  copy-as-markdown button, related pages sidebar
- **Project page** — all sessions for a project with an activity
  heatmap, tool-usage bar chart, token-usage timeline, and topic chips
- **Home page** — 365-day activity heatmap, site-wide stats (total
  tokens, sessions, cache hit ratio), project cards with freshness
  badges
- **Models page** — structured info cards with benchmarks, pricing, and
  auto-generated vs-comparison pages
- **Global search** — Cmd+K command palette with fuzzy matching over a
  pre-built index
- **Dark mode** — system-aware with manual toggle

> **Screenshot reference:** see the [README screenshots](../../README.md#screenshots)
> or the [live demo](https://pratiyush.github.io/llm-wiki/) for the
> visual version of this comparison.

## The pipeline at a glance

```
~/.claude/projects/**/*.jsonl     (raw session transcripts)
         |
         v
    llmwiki sync                  (convert + redact + extract metrics)
         |
         v
    raw/sessions/**/*.md          (clean markdown with frontmatter)
         |
         v
    llmwiki build                 (HTML + CSS + search index + exports)
         |
         v
    site/                         (static site ready to browse or deploy)
     ├── index.html               (home with heatmap + stats)
     ├── sessions/                (one page per session)
     ├── projects/                (one page per project)
     ├── models/                  (structured model profiles)
     ├── vs/                      (auto-generated comparisons)
     ├── search-index.json        (pre-built fuzzy search)
     ├── llms.txt                 (AI agent entry point)
     ├── graph.jsonld             (Schema.org knowledge graph)
     ├── sitemap.xml              (for search engines)
     └── rss.xml                  (for feed readers)
```

## Usage suggestion

When writing a blog post or tweet about llmwiki, screenshot the "Before"
JSONL block and the "After" site side by side. The visual contrast
communicates the value proposition instantly.
