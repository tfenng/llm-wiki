@echo off
REM llmwiki — one-click installer for Windows.
REM Usage: setup.bat
REM Idempotent — safe to re-run.

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ==^> llmwiki setup
echo     root: %cd%

REM 1. Python check
where python >nul 2>&1
if errorlevel 1 (
  echo error: python is required but was not found in PATH
  exit /b 1
)
for /f "delims=" %%v in ('python -c "import sys; print(\".\".join(map(str, sys.version_info[:2])))"') do set PY_VER=%%v
echo     python: !PY_VER!

REM 2. Use the active virtualenv/conda env when present. Otherwise create a
REM    local .venv so system Python restrictions do not break setup.
set "PYTHON_EXE=python"
if not defined VIRTUAL_ENV if not defined CONDA_PREFIX (
  if not exist ".venv\Scripts\python.exe" (
    echo ==^> creating local virtualenv (.venv)
    python -m venv .venv
    if errorlevel 1 exit /b 1
  )
  set "PYTHON_EXE=.venv\Scripts\python.exe"
)

REM 3. Install llmwiki itself so runtime deps come from pyproject.toml.
set "PIP_DISABLE_PIP_VERSION_CHECK=1"
set "PIP_ARGS=-e ."
echo ==^> installing llmwiki build/runtime deps
!PYTHON_EXE! -m pip install --quiet setuptools^>=82.0.1 wheel markdown
if errorlevel 1 exit /b 1
echo ==^> installing llmwiki (!PIP_ARGS!)
!PYTHON_EXE! -m pip install --quiet --no-build-isolation !PIP_ARGS!
if errorlevel 1 exit /b 1
!PYTHON_EXE! -c "import llmwiki, markdown"
if errorlevel 1 exit /b 1

REM 4. Scaffold raw/ wiki/ site/
!PYTHON_EXE! -m llmwiki init
if errorlevel 1 exit /b 1

REM 5. Show available adapters
!PYTHON_EXE! -m llmwiki adapters
if errorlevel 1 exit /b 1

REM 6. Show current sync status so users can see what's ready.
echo.
echo ==^> current sync status:
!PYTHON_EXE! -m llmwiki sync --status --recent 5
if errorlevel 1 exit /b 1

echo.
echo ================================================================
echo   Setup complete.
echo ================================================================
echo.
echo Next steps:
echo   sync.bat                    ^-^- convert new sessions to markdown
echo   build.bat                   ^-^- generate the static HTML site
echo   serve.bat                   ^-^- browse at http://127.0.0.1:8765/
