#!/usr/bin/env bash
# macOS double-clickable command to start the fusion stack (invokes scripts/start_fusion_stack.sh)
set -euo pipefail
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$SCRIPT_DIR"
exec "$REPO_ROOT/scripts/start_fusion_stack.sh" "$@"
