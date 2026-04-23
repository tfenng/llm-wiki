@echo off
REM llmwiki — convert new session transcripts to markdown.
REM Usage: sync.bat [--project <sub>] [--since YYYY-MM-DD] [--include-current] [--force] [--dry-run]
cd /d "%~dp0"
set "PYTHON_EXE=python"
if not defined VIRTUAL_ENV if not defined CONDA_PREFIX (
  if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
)
%PYTHON_EXE% -m llmwiki sync %*
