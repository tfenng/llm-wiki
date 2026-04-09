# llm-wiki GitHub Webhook Handler

A minimal HTTP server that receives GitHub push webhooks and triggers `llmwiki sync` + `llmwiki build` automatically.

## Features

- Stdlib only (no Flask, no dependencies beyond Python 3.9+)
- HMAC signature verification (optional, via `WEBHOOK_SECRET`)
- Health check endpoint at `GET /health`
- Runs sync then build on every push event

## Usage

```bash
# Basic (listens on 0.0.0.0:9876)
python3 handler.py

# Custom port
python3 handler.py --port 9000

# With signature verification
WEBHOOK_SECRET=your-secret python3 handler.py

# Point at a different project directory
LLMWIKI_DIR=/path/to/llm-wiki python3 handler.py
```

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `LLMWIKI_DIR` | `.` (cwd) | Path to the llm-wiki project root |
| `WEBHOOK_SECRET` | *(empty)* | GitHub webhook secret for HMAC verification |
| `PYTHON_PATH` | `python3` | Python interpreter for running llmwiki CLI |

## GitHub Setup

1. Go to your repository **Settings > Webhooks > Add webhook**
2. Set **Payload URL** to `http://your-server:9876/webhook`
3. Set **Content type** to `application/json`
4. Set **Secret** to match your `WEBHOOK_SECRET` value
5. Select "Just the push event"

## Running in Production

For a production deployment, run behind a reverse proxy (nginx, Caddy) with TLS:

```bash
# systemd service example
[Unit]
Description=llmwiki webhook handler
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/llm-wiki/integrations/webhook/handler.py --port 9876
WorkingDirectory=/opt/llm-wiki
Environment=LLMWIKI_DIR=/opt/llm-wiki
Environment=WEBHOOK_SECRET=your-secret
Restart=always

[Install]
WantedBy=multi-user.target
```
