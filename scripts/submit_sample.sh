#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

PROMPT_FILE="$REPO_ROOT/workspace/examples/sample_prompt.txt"

if [[ ! -f "$PROMPT_FILE" ]]; then
  echo "Sample prompt missing at $PROMPT_FILE"
  exit 1
fi

exec "$REPO_ROOT/run_fusion.sh" submit "$(cat "$PROMPT_FILE")"
