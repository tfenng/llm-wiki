---
title: "Jira adapter"
type: navigation
docs_shell: true
---

# Jira adapter

Fetches **Jira tickets** via the REST API and turns each ticket into a
source markdown file.  Useful when part of your decision-making
history lives in Jira alongside the coding sessions.

**Non-AI adapter** (`is_ai_session = False`, #326) — opt-in only, never
fires on a default `sync`.

## What it reads

- Issues from one or more Jira projects via `jira.JIRA` REST client.
- JQL-filtered subsets (e.g. tickets you created / assigned to you /
  updated in the last 30 days).
- Ticket body + comments; attachments are listed but not downloaded.

## Enable it

```jsonc
// sessions_config.json
{
  "jira": {
    "enabled": true,
    "server": "https://your-org.atlassian.net",
    "email": "you@your-org.com",
    "api_token_env": "JIRA_API_TOKEN",
    "jql": "assignee = currentUser() AND updated >= -30d ORDER BY updated DESC",
    "max_results": 500
  }
}
```

Set `JIRA_API_TOKEN` in your `.env`:

```
JIRA_API_TOKEN=<your-token-from-id.atlassian.com>
```

Then:

```bash
llmwiki sync --adapter jira
```

## Output layout

```
raw/sessions/jira/<YYYY-MM-DDTHH-MM>-jira-<ticket-key>.md
```

Frontmatter carries `key`, `summary`, `status`, `reporter`,
`assignee`, `labels`, `created`, `updated`.  Body is the ticket
description + comment timeline.

## Gotchas

- API tokens expire; rotate via id.atlassian.com → Security → API tokens.
- Large JQLs hit rate-limit (~50 req/min on Cloud) — the adapter
  paginates at 50/page; 500 issues ≈ 10 requests.
- Cloud vs Server: adjust `server` URL.  Personal Access Token auth
  (server edition) uses `username` + `password` fields instead of
  `email` + `api_token_env`.

## Code

- `llmwiki/adapters/jira_adapter.py`
- Depends on the `jira` pip package + `jira2markdown` for body rendering
- Issue history: #326 (opt-in by default)

## See also

- [Adapter authoring](../adapter-authoring.md) — if Jira isn't enough,
  write your own REST-pulling adapter.
- [Privacy](../privacy.md) — ticket bodies may contain sensitive
  customer data; check your org's data-handling policy before enabling.
