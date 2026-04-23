@echo off
REM llmwiki — build the static HTML site.
REM Usage: build.bat [--synthesize] [--out <dir>]
cd /d "%~dp0"
set "PYTHON_EXE=python"
if not defined VIRTUAL_ENV if not defined CONDA_PREFIX (
  if exist ".venv\Scripts\python.exe" set "PYTHON_EXE=.venv\Scripts\python.exe"
)
%PYTHON_EXE% -m llmwiki build %*
