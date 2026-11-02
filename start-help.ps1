$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $ProjectRoot

uv run python scripts/build_help_app.py --json
uv run python scripts/serve_help_app.py
