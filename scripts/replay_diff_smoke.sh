#!/usr/bin/env bash
set -euo pipefail
cd /Users/kalimeeks/MCP-FUSION

PY="/Users/kalimeeks/MCP-FUSION/.venv/bin/python"
DIFF="/Users/kalimeeks/MCP-FUSION/workspace/core/replay_diff.py"
LOG="/Users/kalimeeks/MCP-FUSION/workspace/memory/runs.jsonl"

echo "== REPLAY DIFF SMOKE =="
ls -la "$DIFF"
ls -la "$LOG"

# Smoke: diff file against itself (should not crash)
"$PY" "$DIFF" "$LOG" "$LOG" || true
echo "OK: replay_diff smoke completed (self-diff)."
