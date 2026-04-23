@echo off
REM llmwiki — start a local HTTP server on 127.0.0.1:8765.
REM Usage: serve.bat [--port N] [--host H] [--open]
cd /d "%~dp0"
set "PYTHON_EXE=python"
if not defined VIRTUAL_ENV if not defined CONDA_PREFIX (
  if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
)
%PYTHON_EXE% -m llmwiki serve %*
