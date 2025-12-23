#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
MODE="${1:-${FUSION_MODE:-demo}}"
cd "$REPO_ROOT"

FUSION_MODE="$MODE" exec ./run_fusion.sh start
