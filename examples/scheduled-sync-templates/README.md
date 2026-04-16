# Scheduled Sync Templates (legacy reference)

These are **reference templates** kept for documentation. The recommended
way to generate a scheduled sync task for your OS is:

```bash
llmwiki schedule [--platform macos|linux|windows]
```

The generator reads `scheduled_sync` config in `examples/sessions_config.json`
(cadence, hour, minute, paths) and emits the right file for your platform.
See [`docs/scheduled-sync.md`](../../docs/scheduled-sync.md) for install
instructions.

## Files in this directory

| File | Platform | Generator equivalent |
|------|----------|----------------------|
| `launchd.plist` | macOS | `llmwiki schedule --platform macos` |
| `llmwiki-sync.service` + `.timer` | Linux (systemd) | `llmwiki schedule --platform linux` |
| `llmwiki-sync-task.xml` | Windows (Task Scheduler) | `llmwiki schedule --platform windows` |

## Why keep the templates?

- Users doing manual setup on air-gapped machines without llmwiki installed
- CI fixtures for testing the generator output shape
- Historical reference for the default task definition before v1.0
