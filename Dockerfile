# ── build stage ──────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

# Copy only what pip needs to install the package.
COPY pyproject.toml README.md CHANGELOG.md LICENSE ./
COPY llmwiki/ llmwiki/

# Install the package (and its sole runtime dep: markdown>=3.4).
RUN pip install --no-cache-dir .

# ── runtime stage ────────────────────────────────────────────
FROM python:3.12-slim

LABEL maintainer="Pratiyush <pratiyush1@gmail.com>"
LABEL org.opencontainers.image.source="https://github.com/Pratiyush/llm-wiki"
LABEL org.opencontainers.image.description="LLM Wiki — Karpathy-style knowledge base from your AI coding sessions"

WORKDIR /wiki

# Bring over installed packages and the CLI entry-point script.
COPY --from=builder /usr/local/lib/python3.12/site-packages/ \
                    /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/llmwiki /usr/local/bin/llmwiki

# Seed the example sessions so `llmwiki init` has something to demo.
COPY examples/ examples/

# The serve command defaults to port 8765.
EXPOSE 8765

ENTRYPOINT ["llmwiki"]
CMD ["serve", "--host", "0.0.0.0"]
