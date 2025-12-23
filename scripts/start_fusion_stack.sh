#!/usr/bin/env bash
set -euo pipefail

# Simple wrapper to launch the canonical fusion stack
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_PATH="$(dirname "$SCRIPT_DIR")"

cd "$REPO_PATH"
exec "$REPO_PATH/run_fusion.sh" start
