#!/usr/bin/env bash
# [NEW] /Users/kalimeeks/GEMINI-STACK/workspace/MCP-FUSION/run_debug_pipeline.sh
#
# This script runs a minimal, isolated pipeline for debugging.
# It starts only the required services, runs a single job, and then shuts down.
#
# Pipeline: User -> debug_publisher -> [chatgpt] -> [judge] -> User

set -e

# Get the repo root by finding where this script lives
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$SCRIPT_DIR"
BASE_DIR="$REPO_ROOT/workspace"

echo "[DEBUG LAUNCH] MCP-FUSION repo root: $REPO_ROOT"
echo "[DEBUG LAUNCH] MCP-FUSION workspace: $BASE_DIR"
cd "$BASE_DIR"

# --------------------
# Activate virtualenv and load .env
# --------------------
if [ -f ".venv/bin/activate" ]; then
    source ".venv/bin/activate"
else
    echo "[ERROR] .venv not found at $BASE_DIR/.venv"
    exit 1
fi

local env_loader="$REPO_ROOT/scripts/load_env.sh"
if [ -f "$env_loader" ]; then
    source "$env_loader"
else
    echo "[ERROR] Env loader script not found at $env_loader"
    exit 1
fi

# --------------------
# Define Services to Run
# --------------------
SERVICES_TO_RUN=(
    "broker/router.py"
    "agents/chatgpt/worker.py"
    "agents/judge/worker.py"
)

# --------------------
# Start & Manage Services
# --------------------
export PYTHONPATH="$BASE_DIR:$PYTHONPATH"
PIDS=()

# Cleanup function to kill all started processes
cleanup() {
    echo "\n[DEBUG LAUNCH] Shutting down debug services..."
    for pid in "${PIDS[@]}"; do
        kill "$pid" 2>/dev/null || true
    done
    echo "[DEBUG LAUNCH] Cleanup complete."
}
trap cleanup EXIT

# Start the selected services in the background
echo "[DEBUG LAUNCH] Starting debug services..."
for service in "${SERVICES_TO_RUN[@]}"; do
    echo "[DEBUG LAUNCH] --> Starting $service"
    python3 "$service" &
    PIDS+=($!)
done

echo "[DEBUG LAUNCH] All debug services are online."

# --------------------
# Run the Publisher
# --------------------
# This runs in the foreground and will determine the script's exit code
python3 "tools/debug_publisher.py"

echo "[DEBUG LAUNCH] Publisher finished."
# The cleanup trap will handle shutting everything down.
