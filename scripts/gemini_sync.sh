#!/usr/bin/env bash
set -euo pipefail

# Gemini sync helper (safe, non-destructive)
# - Verifies hub path exists
# - If gemini CLI available, forwards args to it
# - Otherwise prints helpful guidance

GEMINI_HUB="/Users/kalimeeks/GEMINI-STACK/workspace"

# 1) Verify the Gemini hub directory exists
if [ ! -d "$GEMINI_HUB" ]; then
  echo "[ERROR] Gemini hub not found at: $GEMINI_HUB"
  echo "Please ensure the Gemini management hub is cloned/available at that path."
  exit 1
fi

echo "Gemini hub found at $GEMINI_HUB"

# 2) Change into the hub (non-destructive)
cd "$GEMINI_HUB"

# 3) If gemini CLI is available, forward arguments
if command -v gemini >/dev/null 2>&1; then
  echo "Running: gemini $*"
  # shellcheck disable=SC2086
  gemini "$@"
else
  echo "[WARN] 'gemini' CLI not found in PATH."
  echo "Install the Gemini CLI or update this script to point to your CLI binary."
  echo "You can still inspect the hub at: $GEMINI_HUB"
  exit 0
fi
