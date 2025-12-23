#!/usr/bin/env bash
#
# fusion_stop.sh - Stop MCP-FUSION Coordinator Worker
#
# Safely stops the coordinator worker using the PID file.
#
# Usage:
#   ./scripts/fusion_stop.sh

set -euo pipefail

# Navigate to repo root
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

PID_DIR="$REPO_ROOT/workspace/memory"
PID_FILE="$PID_DIR/coordinator.pid"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}===== STOPPING FUSION COORDINATOR =====${NC}"
echo

if [ ! -f "$PID_FILE" ]; then
    echo -e "${YELLOW}No PID file found at: $PID_FILE${NC}"
    echo -e "${YELLOW}Coordinator may not be running.${NC}"
    exit 0
fi

PID=$(cat "$PID_FILE")

if ! ps -p "$PID" > /dev/null 2>&1; then
    echo -e "${YELLOW}Coordinator process (PID: $PID) not running.${NC}"
    echo -e "${YELLOW}Removing stale PID file...${NC}"
    rm -f "$PID_FILE"
    exit 0
fi

echo -e "${GREEN}Found coordinator process (PID: $PID)${NC}"
echo -e "${GREEN}Sending SIGTERM...${NC}"

# Send SIGTERM for graceful shutdown
kill -TERM "$PID" 2>/dev/null || true

# Wait up to 5 seconds for graceful shutdown
for i in {1..5}; do
    if ! ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Coordinator stopped gracefully${NC}"
        rm -f "$PID_FILE"
        exit 0
    fi
    sleep 1
done

# Force kill if still running
if ps -p "$PID" > /dev/null 2>&1; then
    echo -e "${YELLOW}Coordinator did not stop gracefully. Sending SIGKILL...${NC}"
    kill -KILL "$PID" 2>/dev/null || true
    sleep 1
fi

# Final check
if ps -p "$PID" > /dev/null 2>&1; then
    echo -e "${RED}✗ Failed to stop coordinator (PID: $PID)${NC}"
    echo -e "${YELLOW}  Manual kill: kill -9 $PID${NC}"
    exit 1
else
    echo -e "${GREEN}✓ Coordinator stopped (forced)${NC}"
    rm -f "$PID_FILE"
fi

echo
echo -e "${GREEN}===== COORDINATOR STOPPED =====${NC}"
