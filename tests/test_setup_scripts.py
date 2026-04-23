"""Installer script regression tests.

These tests keep the one-click setup scripts aligned with the documented
editable-install flow so runtime dependencies (for example ``markdown``)
come from ``pyproject.toml`` instead of ad-hoc manual installs.
"""

from __future__ import annotations

import pytest

from llmwiki import REPO_ROOT


SETUP_SH = REPO_ROOT / "setup.sh"
SETUP_BAT = REPO_ROOT / "setup.bat"
BUILD_SH = REPO_ROOT / "build.sh"
SYNC_SH = REPO_ROOT / "sync.sh"
SERVE_SH = REPO_ROOT / "serve.sh"
BUILD_BAT = REPO_ROOT / "build.bat"
SYNC_BAT = REPO_ROOT / "sync.bat"
SERVE_BAT = REPO_ROOT / "serve.bat"


def test_setup_sh_installs_llmwiki_in_editable_mode():
    text = SETUP_SH.read_text(encoding="utf-8")
    assert "-e ." in text


def test_setup_sh_does_not_ignore_install_failures():
    text = SETUP_SH.read_text(encoding="utf-8")
    assert "pip install --quiet --no-build-isolation -e ." in text
    assert "pip install --quiet --no-build-isolation -e . || true" not in text


def test_setup_sh_hook_uses_sync_wrapper():
    text = SETUP_SH.read_text(encoding="utf-8")
    assert "sync.sh > /tmp/llmwiki-sync.log" in text
    assert "llmwiki/convert.py" not in text


def test_setup_scripts_do_not_override_pip_index_config():
    assert "PIP_INDEX_URL" not in SETUP_SH.read_text(encoding="utf-8")
    assert "PIP_INDEX_URL" not in SETUP_BAT.read_text(encoding="utf-8")


def test_setup_bat_installs_llmwiki_in_editable_mode():
    text = SETUP_BAT.read_text(encoding="utf-8")
    assert "-e ." in text


@pytest.mark.parametrize("script", [SETUP_SH, BUILD_SH, SYNC_SH, SERVE_SH])
def test_shell_scripts_support_local_dot_venv(script):
    text = script.read_text(encoding="utf-8")
    assert ".venv" in text


@pytest.mark.parametrize("script", [SETUP_BAT, BUILD_BAT, SYNC_BAT, SERVE_BAT])
def test_batch_scripts_support_local_dot_venv(script):
    text = script.read_text(encoding="utf-8")
    assert ".venv" in text.lower()


@pytest.mark.parametrize("script", [BUILD_BAT, SYNC_BAT, SERVE_BAT])
def test_batch_wrappers_prefer_active_virtualenv(script):
    text = script.read_text(encoding="utf-8")
    assert "VIRTUAL_ENV" in text
    assert "CONDA_PREFIX" in text


def test_setup_bat_stops_on_post_install_failures():
    text = SETUP_BAT.read_text(encoding="utf-8")
    assert "!PYTHON_EXE! -m llmwiki init\nif errorlevel 1 exit /b 1" in text
    assert "!PYTHON_EXE! -m llmwiki adapters\nif errorlevel 1 exit /b 1" in text
    assert "!PYTHON_EXE! -m llmwiki sync --status --recent 5\nif errorlevel 1 exit /b 1" in text
