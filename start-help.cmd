@echo off
cd /d "%~dp0"
uv run python scripts\build_help_app.py --json || exit /b 1
uv run python scripts\serve_help_app.py
