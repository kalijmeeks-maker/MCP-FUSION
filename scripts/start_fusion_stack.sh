#!/usr/bin/env bash

# Get repo root dynamically (parent of scripts/)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_PATH="$(dirname "$SCRIPT_DIR")"

# 1. Go to repo root
cd "$REPO_PATH" || {
    echo "[ERROR] Could not cd to $REPO_PATH"
    exit 1
}

echo "[HOST] In repo: $(pwd)"

# 2. Make sure Docker stack is up (detached)
echo "[HOST] Starting docker compose..."
docker compose up -d

echo "[HOST] Current containers:"
docker ps

SESSION="mcp-fusion"

# 3. Start a tmux session with 4 panes
#    Pane 0: Redis MONITOR (inside redis container)
#    Pane 1: redis_bridge.py (inside fusion container → /workspace/broker)
#    Pane 2: sim_driver.py (inside fusion container → /workspace/sim)
#    Pane 3: llama_loop.py (inside fusion container → /workspace/loop)

# If a previous tmux session exists, kill it so we create a clean layout.
if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "[HOST] Existing tmux session $SESSION found — killing and recreating"
    tmux kill-session -t "$SESSION" || true
fi

# Small pause to ensure tmux server settled
sleep 0.2

# Create the tmux session
tmux new-session -d -s "$SESSION" \
    "cd '$REPO_PATH' && docker exec -it mcp-fusion-redis-1 redis-cli MONITOR"

# Right split: broker / redis_bridge
tmux split-window -h \
    "cd '$REPO_PATH' && docker exec -it mcp-fusion-fusion-1 bash -lc 'cd /workspace/broker && pwd && python3 redis_bridge.py'"

# Bottom split under left: sim / sim_driver
tmux select-pane -t 0
tmux split-window -v \
    "cd '$REPO_PATH' && docker exec -it mcp-fusion-fusion-1 bash -lc 'cd /workspace/sim && pwd && python3 sim_driver.py --test-publish'"

# Bottom split under right: loop / llama_loop
tmux select-pane -t 1
tmux split-window -v \
    "cd '$REPO_PATH' && docker exec -it mcp-fusion-fusion-1 bash -lc 'cd /workspace/loop && pwd && python3 llama_loop.py'"

# Optional: arrange layout nicely
tmux select-layout tiled

# Attach so you see all 4 panes
tmux attach-session -t "$SESSION"
