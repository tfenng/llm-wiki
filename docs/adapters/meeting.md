---
title: "Meeting transcript adapter"
type: navigation
docs_shell: true
---

# Meeting transcript adapter

Ingests **VTT / SRT / plain-text transcripts** from meeting recordings
so your meeting history ends up in the same wiki as your coding
sessions.

**Non-AI adapter** (`is_ai_session = False`, #326) — opt-in only.

## What it reads

- `.vtt` — WebVTT files from Zoom, Google Meet, Teams.
- `.srt` — SubRip subtitle files from most recording tools.
- `.txt` — plain-text transcripts with `HH:MM:SS Speaker: …` lines.

Speaker tags + timestamps are preserved in the output so `/wiki-query`
can answer "what did Alice say about retries?".

## Enable it

```jsonc
// sessions_config.json
{
  "meeting": {
    "enabled": true,
    "transcripts_dir": "~/meetings",
    "default_speaker": "Speaker"
  }
}
```

Drop transcripts into `~/meetings/` (flat or nested by project).  Then:

```bash
llmwiki sync --adapter meeting
```

## Output layout

```
raw/sessions/meeting/<YYYY-MM-DDTHH-MM>-meeting-<slug>.md
```

`<slug>` is derived from the filename (e.g. `2026-04-17-design-review.vtt`
→ `design-review`).  Frontmatter: `speakers` (comma-separated list),
`duration_seconds`, `recorded_at` (parsed from filename when
`YYYY-MM-DD` prefix is present, else falls back to file mtime).

## Gotchas

- Plain-text transcripts must follow `HH:MM:SS Speaker: text` per line
  — different conventions (e.g. `[00:00:12] Alice:`) need a custom
  parser.
- No speaker diarisation — if the transcript labels everyone as
  `Speaker 1 / Speaker 2` you'll get generic labels; fix in the source
  tool.
- Long meetings split across multiple files are treated as separate
  sources; the `--project` flag groups them in the wiki if you follow
  a consistent filename prefix.

## Code

- `llmwiki/adapters/meeting.py`
- Tests: `tests/test_meeting_adapter.py`

## See also

- [Privacy](../privacy.md) — transcripts often quote co-workers
  directly. Consider redacting names or keeping meeting transcripts
  local-only.
