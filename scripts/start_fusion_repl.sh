#!/usr/bin/env bash
#
# start_fusion_repl.sh - Launch MCP-FUSION REPL with coordinator
#
# This script sets up and launches the complete MCP-FUSION REPL environment:
# 1. Verifies environment setup
# 2. Checks Redis connectivity
# 3. Starts coordinator worker in background
# 4. Launches interactive REPL
#
# Usage:
#   ./scripts/start_fusion_repl.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$REPO_ROOT"

echo "===== FUSION REPL IGNITION ====="
echo

# Step 0: Check Python environment
echo "== 0) PYTHON ENVIRONMENT =="
if [ -d ".venv" ] && [ -x ".venv/bin/python" ]; then
    PYTHON_BIN="$REPO_ROOT/.venv/bin/python"
    echo "✓ Using venv: $PYTHON_BIN"
    "$PYTHON_BIN" -c "import sys; print(f'  Python: {sys.version}')"
else
    echo "⚠ No .venv found, using system python3"
    PYTHON_BIN="python3"
    if ! command -v python3 &> /dev/null; then
        echo "ERROR: python3 not found. Install Python 3 or create venv."
        exit 1
    fi
fi
echo

# Step 1: Verify environment
echo "== 1) ENVIRONMENT VERIFICATION =="
if [ -f "$SCRIPT_DIR/verify.sh" ]; then
    chmod +x "$SCRIPT_DIR/verify.sh" 2>/dev/null || true
    "$SCRIPT_DIR/verify.sh" || {
        echo "ERROR: Environment verification failed"
        exit 1
    }
else
    echo "⚠ verify.sh not found, skipping verification"
fi
echo

# Step 2: Redis connectivity check
echo "== 2) REDIS CONNECTIVITY =="
if command -v redis-cli &> /dev/null; then
    if redis-cli PING 2>/dev/null | grep -q PONG; then
        echo "✓ Redis: PONG"
    else
        echo "ERROR: Redis not responding. Start with: redis-server"
        echo "Or use Docker: docker compose up -d"
        exit 1
    fi
else
    echo "ERROR: redis-cli not found. Install Redis or use Docker."
    exit 1
fi
echo

# Step 3: Create memory directory for logs
echo "== 3) SETUP LOGGING =="
LOGDIR="$REPO_ROOT/workspace/memory"
mkdir -p "$LOGDIR"
COORD_LOG="$LOGDIR/coordinator_$(date +%Y%m%d_%H%M%S).log"
echo "✓ Log directory: $LOGDIR"
echo "  Coordinator log: $COORD_LOG"
echo

# Step 4: Start coordinator worker (if not already running)
echo "== 4) COORDINATOR WORKER =="
if pgrep -f "coordinator_worker" &>/dev/null; then
    echo "✓ Coordinator already running"
else
    echo "→ Starting coordinator worker in background..."
    nohup "$PYTHON_BIN" -m workspace.workers.coordinator_worker > "$COORD_LOG" 2>&1 &
    COORD_PID=$!
    echo "✓ Coordinator started (PID: $COORD_PID)"
    echo "  Monitor log: tail -f $COORD_LOG"
    
    # Give it a moment to initialize
    sleep 1
    
    # Check if it's still running
    if ! ps -p $COORD_PID &>/dev/null; then
        echo "ERROR: Coordinator failed to start. Check log:"
        tail -n 20 "$COORD_LOG"
        exit 1
    fi
fi
echo

# Step 5: Send a smoke test task
echo "== 5) SMOKE TEST =="
TEST_TASK='{"task":"Explain the current MCP-FUSION architecture and output strict JSON.","constraints":{"format":"json","no_markdown":true}}'
redis-cli LPUSH fusion_tasks "$TEST_TASK" &>/dev/null
echo "→ Smoke test task submitted"
sleep 1

# Check for result
RESULT=$(redis-cli LRANGE plasma_results 0 0 2>/dev/null || echo "")
if [ -n "$RESULT" ] && [ "$RESULT" != "(empty array)" ]; then
    echo "✓ Coordinator responding"
else
    echo "⚠ No response yet (coordinator may still be initializing)"
fi
echo

# Step 6: Launch REPL
echo "== 6) LAUNCHING REPL =="
echo "Type prompts at the fusion> prompt"
echo "Press Ctrl+C to exit"
echo "=" * 60
echo

# Make sure fusion_repl.py exists and is executable
if [ ! -f "$SCRIPT_DIR/fusion_repl.py" ]; then
    echo "ERROR: fusion_repl.py not found at $SCRIPT_DIR/fusion_repl.py"
    exit 1
fi

chmod +x "$SCRIPT_DIR/fusion_repl.py" 2>/dev/null || true

# Launch the REPL
exec "$PYTHON_BIN" "$SCRIPT_DIR/fusion_repl.py"
