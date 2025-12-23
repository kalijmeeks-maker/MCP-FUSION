#!/usr/bin/env bash
# macOS double-clickable command to start the fusion stack (wraps run_fusion.sh start)
# Requires workspace/.venv and workspace/.env to be set up (run ./run_fusion.sh bootstrap first).
set -euo pipefail
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$SCRIPT_DIR"
exec "$REPO_ROOT/scripts/start_fusion_stack.sh" "$@"
