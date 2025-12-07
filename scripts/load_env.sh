#!/bin/bash
# Load environment variables from the .env file
# This script can be sourced by other scripts to set up the environment

# Get the repo root (parent of scripts/)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$REPO_ROOT/workspace/.env"

if [ -f "$ENV_FILE" ]; then
    # Use 'set -a' to automatically export all variables
    set -a
    source "$ENV_FILE"
    set +a
    echo "[ENV] Loaded from $ENV_FILE"
else
    echo "[ERROR] .env file not found at $ENV_FILE" >&2
    exit 1
fi
