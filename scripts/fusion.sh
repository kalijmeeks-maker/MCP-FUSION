#!/usr/bin/env bash
#
# fusion.sh - Canonical MCP-FUSION Launcher
#
# The ONE TRUE launcher for MCP-FUSION interactive CLI.
# Manages venv, verifies environment, starts coordinator, provides chat-like REPL.
#
# Usage:
#   ./scripts/fusion.sh              # Start interactive session
#   FUSION_KILL=1 ./scripts/fusion.sh  # Stop coordinator and exit
#   FUSION_TIMEOUT_SEC=60 ./scripts/fusion.sh  # Custom timeout
#
# Environment Variables:
#   FUSION_KILL        - Set to 1 to stop coordinator and exit immediately
#   FUSION_TIMEOUT_SEC - Timeout for waiting on results (default: 30)
#   FUSION_MODEL       - Optional model override

set -euo pipefail

# Navigate to repo root (portable)
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Configuration
VENV_DIR="$REPO_ROOT/.venv"
VENV_PYTHON="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/pip"
REQUIREMENTS="$REPO_ROOT/requirements.txt"
PID_DIR="$REPO_ROOT/workspace/memory"
PID_FILE="$PID_DIR/coordinator.pid"
TASK_LIST="${FUSION_TASK_LIST:-fusion_tasks}"
RESULT_LIST="${FUSION_RESULT_LIST:-plasma_results}"
TIMEOUT="${FUSION_TIMEOUT_SEC:-30}"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Kill mode check
if [ "${FUSION_KILL:-0}" = "1" ]; then
    echo -e "${YELLOW}FUSION_KILL=1 detected. Stopping coordinator...${NC}"
    if [ -f "$REPO_ROOT/scripts/fusion_stop.sh" ]; then
        "$REPO_ROOT/scripts/fusion_stop.sh"
    else
        echo -e "${RED}Error: fusion_stop.sh not found${NC}"
        exit 1
    fi
    exit 0
fi

echo -e "${BLUE}===== MCP-FUSION LAUNCHER =====${NC}"
echo

# Step 1: Assert .venv exists; create if missing
echo -e "${GREEN}[1/6] Checking Python virtual environment...${NC}"
if [ ! -d "$VENV_DIR" ] || [ ! -x "$VENV_PYTHON" ]; then
    echo -e "${YELLOW}  Virtual environment not found. Creating...${NC}"
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}  ✓ Virtual environment created${NC}"
fi

if [ ! -f "$REQUIREMENTS" ]; then
    echo -e "${RED}  Error: requirements.txt not found at $REQUIREMENTS${NC}"
    exit 1
fi

# Install/upgrade dependencies
echo -e "${GREEN}  Installing dependencies...${NC}"
"$VENV_PIP" install -q --upgrade pip
"$VENV_PIP" install -q -r "$REQUIREMENTS"
echo -e "${GREEN}  ✓ Dependencies installed${NC}"
echo

# Step 2: Run verify.sh
echo -e "${GREEN}[2/6] Running environment verification...${NC}"
if [ -f "$REPO_ROOT/scripts/verify.sh" ]; then
    chmod +x "$REPO_ROOT/scripts/verify.sh"
    if ! "$REPO_ROOT/scripts/verify.sh"; then
        echo -e "${RED}  Verification failed. Fix issues above before continuing.${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}  Warning: verify.sh not found, skipping verification${NC}"
fi
echo

# Step 3: Ensure Redis is reachable
echo -e "${GREEN}[3/6] Checking Redis connectivity...${NC}"
if ! command -v redis-cli &> /dev/null; then
    echo -e "${RED}  Error: redis-cli not found in PATH${NC}"
    echo -e "${YELLOW}  Fix: Install Redis:${NC}"
    echo "    - macOS: brew install redis && brew services start redis"
    echo "    - Ubuntu/Debian: sudo apt-get install redis-server && sudo systemctl start redis"
    echo "    - Docker: docker run -d -p 6379:6379 redis:latest"
    exit 1
fi

if ! redis-cli -h localhost -p 6379 PING &> /dev/null; then
    echo -e "${RED}  Error: Redis not reachable at localhost:6379${NC}"
    echo -e "${YELLOW}  Fix commands:${NC}"
    echo "    - Start Redis server: redis-server"
    echo "    - Or via Docker: docker run -d -p 6379:6379 redis:latest"
    echo "    - Or via Docker Compose: docker compose up -d"
    exit 1
fi
echo -e "${GREEN}  ✓ Redis responding to PING${NC}"
echo

# Step 4: Start coordinator worker in background
echo -e "${GREEN}[4/6] Starting coordinator worker...${NC}"
mkdir -p "$PID_DIR"

# Check if coordinator already running
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}  Coordinator already running (PID: $OLD_PID)${NC}"
    else
        echo -e "${YELLOW}  Stale PID file found, removing...${NC}"
        rm -f "$PID_FILE"
    fi
fi

# Start coordinator if not running
if [ ! -f "$PID_FILE" ] || ! ps -p "$(cat "$PID_FILE" 2>/dev/null)" > /dev/null 2>&1; then
    LOG_FILE="$PID_DIR/coordinator_$(date +%Y%m%d_%H%M%S).log"
    nohup "$VENV_PYTHON" -m workspace.workers.coordinator_worker > "$LOG_FILE" 2>&1 &
    COORDINATOR_PID=$!
    echo "$COORDINATOR_PID" > "$PID_FILE"
    echo -e "${GREEN}  ✓ Coordinator started (PID: $COORDINATOR_PID)${NC}"
    echo -e "${GREEN}    Log: $LOG_FILE${NC}"
    sleep 2  # Give coordinator time to initialize
else
    echo -e "${GREEN}  ✓ Coordinator already running${NC}"
fi
echo

# Step 5: Clear old tasks/results
echo -e "${GREEN}[5/6] Clearing old queues...${NC}"
redis-cli DEL "$TASK_LIST" > /dev/null 2>&1 || true
redis-cli DEL "$RESULT_LIST" > /dev/null 2>&1 || true
echo -e "${GREEN}  ✓ Queues cleared${NC}"
echo

# Step 6: Interactive prompt loop
echo -e "${GREEN}[6/6] Launching interactive REPL...${NC}"
echo -e "${BLUE}===== FUSION REPL ACTIVE =====${NC}"
echo -e "${YELLOW}Type your prompt and press Enter. Ctrl+C to exit.${NC}"
echo -e "${YELLOW}Queue: $TASK_LIST → $RESULT_LIST (timeout: ${TIMEOUT}s)${NC}"
echo

# Interactive loop
while true; do
    # Read user input
    echo -ne "${BLUE}fusion>${NC} "
    read -r USER_PROMPT || break
    
    # Skip empty input
    if [ -z "$USER_PROMPT" ]; then
        continue
    fi
    
    # Build task payload
    TASK_PAYLOAD=$(cat <<EOF
{"task":"$USER_PROMPT","constraints":{"format":"json","no_markdown":false}}
EOF
)
    
    # Add optional model override
    if [ -n "${FUSION_MODEL:-}" ]; then
        TASK_PAYLOAD=$(echo "$TASK_PAYLOAD" | sed "s/\"constraints\":/\"model\":\"$FUSION_MODEL\",\"constraints\":/")
    fi
    
    # Publish task
    echo -e "${YELLOW}  ⏳ Processing...${NC}"
    redis-cli LPUSH "$TASK_LIST" "$TASK_PAYLOAD" > /dev/null
    
    # Wait for result with timeout
    RESULT=$(redis-cli BLPOP "$RESULT_LIST" "$TIMEOUT" 2>/dev/null || echo "")
    
    if [ -z "$RESULT" ]; then
        echo -e "${RED}  ✗ Timeout waiting for result (${TIMEOUT}s)${NC}"
        echo -e "${YELLOW}    Check coordinator log: $PID_DIR/coordinator_*.log${NC}"
        continue
    fi
    
    # Parse result (format: "queue_name" "json_data")
    RESULT_JSON=$(echo "$RESULT" | sed 's/^[^ ]* //')
    
    # Extract response text from JSON
    if command -v jq &> /dev/null; then
        # Use jq if available for clean parsing
        OUTPUT_TEXT=$(echo "$RESULT_JSON" | jq -r '.response // .message // .task // "No response"' 2>/dev/null || echo "$RESULT_JSON")
    else
        # Fallback: simple grep-based extraction
        OUTPUT_TEXT=$(echo "$RESULT_JSON" | grep -o '"response":"[^"]*"' | sed 's/"response":"\(.*\)"/\1/' || echo "$RESULT_JSON")
    fi
    
    # Display output
    echo -e "${GREEN}  ✓ ${OUTPUT_TEXT}${NC}"
    echo
done

echo -e "\n${YELLOW}Exiting Fusion REPL.${NC}"
echo -e "${YELLOW}Coordinator still running. Stop with: ./scripts/fusion_stop.sh${NC}"
