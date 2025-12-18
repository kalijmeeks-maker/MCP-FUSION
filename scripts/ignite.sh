#!/usr/bin/env bash
set -euo pipefail

REPO="/Users/kalimeeks/MCP-FUSION"
PY="$REPO/.venv/bin/python"

cd "$REPO"

echo "===== MCP-FUSION IGNITE ====="
echo "Repo: $REPO"
echo "Branch: $(git branch --show-current)"
echo

# Enforce wip/*
BR="$(git branch --show-current)"
if [[ "$BR" != wip/* ]]; then
  echo "ERROR: Not on wip/* branch. Current: $BR"
  exit 1
fi

# Runtime truth
echo "== Runtime truth =="
"$PY" - << "PY"
import sys
print(sys.executable)
assert ".venv/bin/python" in sys.executable
PY
echo

# Verify
echo "== verify.sh =="
chmod +x "$REPO/scripts/verify.sh"
"$REPO/scripts/verify.sh"
echo

# Ignite (Stage-1/2)
echo "== RUN coordinator_worker (module) =="
exec "$PY" -m workspace.workers.coordinator_worker
