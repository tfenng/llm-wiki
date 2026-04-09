"""Tests for integrations/webhook/handler.py."""

from __future__ import annotations

import hashlib
import hmac
import json
import sys
from http.server import HTTPServer
from pathlib import Path
from threading import Thread
from urllib.request import Request, urlopen

import pytest

# Add the webhook integration to the path so we can import handler
WEBHOOK_DIR = Path(__file__).resolve().parent.parent / "integrations" / "webhook"
sys.path.insert(0, str(WEBHOOK_DIR))

import handler  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def server_port() -> int:
    """Find a free port."""
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


@pytest.fixture()
def webhook_server(server_port: int, monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Start the webhook handler on a random port, pointed at a temp dir."""
    monkeypatch.setattr(handler, "LLMWIKI_DIR", tmp_path)
    monkeypatch.setattr(handler, "WEBHOOK_SECRET", "")
    # Override _run_llmwiki to be a no-op so tests don't need llmwiki installed
    monkeypatch.setattr(
        handler.WebhookHandler,
        "_run_llmwiki",
        lambda self, cmd: None,
    )

    srv = HTTPServer(("127.0.0.1", server_port), handler.WebhookHandler)
    thread = Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    yield srv
    srv.shutdown()


def _post(port: int, path: str, body: dict, headers: dict | None = None) -> tuple[int, dict]:
    """Send a POST request and return (status_code, json_body)."""
    data = json.dumps(body).encode("utf-8")
    req = Request(
        f"http://127.0.0.1:{port}{path}",
        data=data,
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    try:
        resp = urlopen(req)
        return resp.status, json.loads(resp.read())
    except Exception as e:
        # urllib raises on 4xx/5xx
        if hasattr(e, "code") and hasattr(e, "read"):
            return e.code, json.loads(e.read())  # type: ignore[union-attr]
        raise


def _get(port: int, path: str) -> tuple[int, dict]:
    """Send a GET request."""
    req = Request(f"http://127.0.0.1:{port}{path}")
    resp = urlopen(req)
    return resp.status, json.loads(resp.read())


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestHealthEndpoint:
    def test_health_returns_ok(self, webhook_server: HTTPServer, server_port: int) -> None:
        status, body = _get(server_port, "/health")
        assert status == 200
        assert body["status"] == "healthy"

    def test_root_returns_status(self, webhook_server: HTTPServer, server_port: int) -> None:
        status, body = _get(server_port, "/")
        assert status == 200


class TestPushWebhook:
    def test_push_triggers_sync(self, webhook_server: HTTPServer, server_port: int) -> None:
        status, body = _post(
            server_port,
            "/webhook",
            {"ref": "refs/heads/main"},
            {"X-GitHub-Event": "push"},
        )
        assert status == 200
        assert body["status"] == "ok"

    def test_non_push_event_ignored(self, webhook_server: HTTPServer, server_port: int) -> None:
        status, body = _post(
            server_port,
            "/webhook",
            {"action": "opened"},
            {"X-GitHub-Event": "pull_request"},
        )
        assert status == 200
        assert body["status"] == "ignored"

    def test_wrong_path_returns_404(self, webhook_server: HTTPServer, server_port: int) -> None:
        status, body = _post(server_port, "/wrong", {}, {})
        assert status == 404


class TestSignatureVerification:
    def test_valid_signature_accepted(
        self, server_port: int, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        secret = "test-secret-123"
        monkeypatch.setattr(handler, "LLMWIKI_DIR", tmp_path)
        monkeypatch.setattr(handler, "WEBHOOK_SECRET", secret)
        monkeypatch.setattr(
            handler.WebhookHandler,
            "_run_llmwiki",
            lambda self, cmd: None,
        )

        srv = HTTPServer(("127.0.0.1", server_port), handler.WebhookHandler)
        thread = Thread(target=srv.serve_forever, daemon=True)
        thread.start()

        payload = json.dumps({"ref": "refs/heads/main"}).encode("utf-8")
        sig = "sha256=" + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()

        status, body = _post(
            server_port,
            "/webhook",
            {"ref": "refs/heads/main"},
            {"X-GitHub-Event": "push", "X-Hub-Signature-256": sig},
        )
        assert status == 200
        srv.shutdown()

    def test_invalid_signature_rejected(
        self, server_port: int, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        monkeypatch.setattr(handler, "LLMWIKI_DIR", tmp_path)
        monkeypatch.setattr(handler, "WEBHOOK_SECRET", "real-secret")

        srv = HTTPServer(("127.0.0.1", server_port), handler.WebhookHandler)
        thread = Thread(target=srv.serve_forever, daemon=True)
        thread.start()

        status, body = _post(
            server_port,
            "/webhook",
            {"ref": "refs/heads/main"},
            {"X-GitHub-Event": "push", "X-Hub-Signature-256": "sha256=wrong"},
        )
        assert status == 403
        assert body["error"] == "invalid signature"
        srv.shutdown()
