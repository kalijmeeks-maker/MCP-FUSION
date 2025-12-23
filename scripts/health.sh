#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
MODE="${FUSION_MODE:-demo}"
cd "$REPO_ROOT"

ensure_redis() {
  if ./run_fusion.sh status >/dev/null 2>&1; then
    return
  fi
}

if [[ "$MODE" == "demo" ]]; then
  export FUSION_HEALTH_ALLOW_STOPPED=1
else
  export FUSION_HEALTH_ALLOW_STOPPED=0
fi

ensure_redis
FUSION_MODE="$MODE" exec ./run_fusion.sh health
