#!/usr/bin/env bash
#
# health.sh - MCP-FUSION Health Check
#
# Prints system status including Python, Redis, verification status,
# and recent run history.
#
# Usage:
#   ./scripts/health.sh

set -euo pipefail

# Navigate to repo root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

VENV_PYTHON="$REPO_ROOT/.venv/bin/python"
PID_FILE="$REPO_ROOT/workspace/memory/coordinator.pid"
RUNS_LOG="$REPO_ROOT/workspace/memory/runs.jsonl"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}===== MCP-FUSION HEALTH CHECK =====${NC}"
echo

# Check 1: Python executable
echo -e "${GREEN}[Python Executable]${NC}"
if [ -x "$VENV_PYTHON" ]; then
    PYTHON_PATH=$("$VENV_PYTHON" -c "import sys; print(sys.executable)")
    PYTHON_VERSION=$("$VENV_PYTHON" --version 2>&1)
    echo -e "  ✓ Path: $PYTHON_PATH"
    echo -e "  ✓ Version: $PYTHON_VERSION"
else
    echo -e "${RED}  ✗ Virtual environment not found or not executable${NC}"
    echo -e "${YELLOW}    Run: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt${NC}"
fi
echo

# Check 2: Redis connectivity
echo -e "${GREEN}[Redis Status]${NC}"
if command -v redis-cli &> /dev/null; then
    if redis-cli PING &> /dev/null; then
        REDIS_VERSION=$(redis-cli INFO server 2>/dev/null | grep "redis_version:" | cut -d: -f2 | tr -d '\r')
        echo -e "  ✓ Redis responding to PING"
        if [ -n "$REDIS_VERSION" ]; then
            echo -e "  ✓ Version: $REDIS_VERSION"
        fi
        
        # Check queue sizes
        TASK_COUNT=$(redis-cli LLEN fusion_tasks 2>/dev/null || echo "0")
        RESULT_COUNT=$(redis-cli LLEN plasma_results 2>/dev/null || echo "0")
        echo -e "  ✓ Queue sizes:"
        echo -e "    - fusion_tasks: $TASK_COUNT"
        echo -e "    - plasma_results: $RESULT_COUNT"
    else
        echo -e "${RED}  ✗ Redis server not responding${NC}"
        echo -e "${YELLOW}    Start: redis-server${NC}"
    fi
else
    echo -e "${RED}  ✗ redis-cli not found in PATH${NC}"
    echo -e "${YELLOW}    Install: brew install redis (macOS) or apt-get install redis-server (Linux)${NC}"
fi
echo

# Check 3: Coordinator status
echo -e "${GREEN}[Coordinator Worker]${NC}"
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "  ✓ Running (PID: $PID)"
        # Get process info
        if command -v ps &> /dev/null; then
            START_TIME=$(ps -p "$PID" -o lstart= 2>/dev/null || echo "Unknown")
            CPU_TIME=$(ps -p "$PID" -o cputime= 2>/dev/null || echo "Unknown")
            echo -e "  ✓ Started: $START_TIME"
            echo -e "  ✓ CPU Time: $CPU_TIME"
        fi
    else
        echo -e "${YELLOW}  ⚠ PID file exists but process not running${NC}"
        echo -e "${YELLOW}    Stale PID: $PID${NC}"
    fi
else
    echo -e "${YELLOW}  ⚠ Not running (no PID file)${NC}"
    echo -e "${YELLOW}    Start: ./scripts/fusion.sh${NC}"
fi
echo

# Check 4: Verify.sh status
echo -e "${GREEN}[Environment Verification]${NC}"
if [ -f "$REPO_ROOT/scripts/verify.sh" ]; then
    chmod +x "$REPO_ROOT/scripts/verify.sh" 2>/dev/null || true
    if "$REPO_ROOT/scripts/verify.sh" > /dev/null 2>&1; then
        echo -e "  ✓ verify.sh: PASS"
    else
        echo -e "${YELLOW}  ⚠ verify.sh: FAIL (run manually for details)${NC}"
    fi
else
    echo -e "${YELLOW}  ⚠ verify.sh not found${NC}"
fi
echo

# Check 5: Recent runs from runs.jsonl
echo -e "${GREEN}[Recent Runs]${NC}"
if [ -f "$RUNS_LOG" ]; then
    RUN_COUNT=$(wc -l < "$RUNS_LOG" 2>/dev/null || echo "0")
    echo -e "  ✓ Total runs logged: $RUN_COUNT"
    echo -e "  ✓ Last 5 runs:"
    
    if command -v jq &> /dev/null; then
        # Use jq for pretty formatting if available
        tail -5 "$RUNS_LOG" | while IFS= read -r line; do
            TIMESTAMP=$(echo "$line" | jq -r '.timestamp // "N/A"' 2>/dev/null)
            TASK=$(echo "$line" | jq -r '.task // "N/A"' 2>/dev/null | cut -c1-50)
            STATUS=$(echo "$line" | jq -r '.status // "N/A"' 2>/dev/null)
            echo -e "    - [$TIMESTAMP] $STATUS: ${TASK}..."
        done
    else
        # Fallback: simple line output
        tail -5 "$RUNS_LOG" | nl -w2 -s'. '
    fi
else
    echo -e "${YELLOW}  ⚠ No runs.jsonl file found${NC}"
    echo -e "${YELLOW}    File will be created on first run${NC}"
fi
echo

# Check 6: Disk space for logs
echo -e "${GREEN}[Disk Space]${NC}"
if [ -d "$REPO_ROOT/workspace/memory" ]; then
    LOG_SIZE=$(du -sh "$REPO_ROOT/workspace/memory" 2>/dev/null | cut -f1 || echo "Unknown")
    echo -e "  ✓ Log directory size: $LOG_SIZE"
else
    echo -e "${YELLOW}  ⚠ Log directory not found${NC}"
fi

# Available disk space
if command -v df &> /dev/null; then
    DISK_AVAIL=$(df -h "$REPO_ROOT" | tail -1 | awk '{print $4}')
    echo -e "  ✓ Available disk space: $DISK_AVAIL"
fi
echo

echo -e "${BLUE}===== HEALTH CHECK COMPLETE =====${NC}"
echo
echo -e "${YELLOW}Quick Commands:${NC}"
echo -e "  Start:  ./scripts/fusion.sh"
echo -e "  Stop:   ./scripts/fusion_stop.sh"
echo -e "  Health: ./scripts/health.sh"
