#!/bin/zsh

echo "=========================================="
echo "🚀 MCP-FUSION AUTOLAUNCH STARTING"
echo "=========================================="

# ---------------------------
# 1) cd into workspace
# ---------------------------
cd /Users/kalimeeks/MCP-FUSION/workspace || {
  echo "❌ Could not enter workspace directory!"
  exit 1
}

# ---------------------------
# 2) Load .env variables
# ---------------------------
if [[ -f ".env" ]]; then
    echo "🔐 Loading API keys from .env..."
    export $(grep -v '^#' .env | xargs)
else
    echo "❌ ERROR: .env file missing!"
    echo "Create it using:"
    echo "  nano /Users/kalimeeks/MCP-FUSION/workspace/.env"
    exit 1
fi

# ---------------------------
# 3) Activate virtual environment
# ---------------------------
echo "🐍 Activating venv..."
source /Users/kalimeeks/MCP-FUSION/workspace/.venv/bin/activate

# ---------------------------
# 4) Export PYTHONPATH
# ---------------------------
export PYTHONPATH="/Users/kalimeeks/MCP-FUSION/workspace:${PYTHONPATH}"
echo "📚 PYTHONPATH set."

# ---------------------------
# 5) Start Redis
# ---------------------------
echo "📡 Starting Redis..."
brew services start redis

# Wait 2s
sleep 2

# ---------------------------
# 6) Start all agents in background
# ---------------------------
echo "🤖 Starting Broker..."
python3 /Users/kalimeeks/MCP-FUSION/workspace/broker/router.py &
BROKER_PID=$!

echo "🤖 Starting Grok Worker..."
python3 /Users/kalimeeks/MCP-FUSION/workspace/agents/grok/worker.py &
GROK_PID=$!

echo "🤖 Starting ChatGPT Worker..."
python3 /Users/kalimeeks/MCP-FUSION/workspace/agents/chatgpt/worker.py &
CHATGPT_PID=$!

echo "🤖 Starting Judge Worker..."
python3 /Users/kalimeeks/MCP-FUSION/workspace/agents/judge/worker.py &
JUDGE_PID=$!

echo "📡 Starting Results Listener..."
python3 /Users/kalimeeks/MCP-FUSION/workspace/sim/grok_results_listener.py &
LISTENER_PID=$!

echo "🧠 Starting Memory Engine..."
python3 /Users/kalimeeks/MCP-FUSION/workspace/sim/memory_engine.py &
MEMORY_PID=$!

# ---------------------------
# 7) Start the Orchestrator last
# ---------------------------
echo "🎛️ Starting Orchestrator..."
python3 /Users/kalimeeks/MCP-FUSION/workspace/sim/orchestrator.py &
ORCH_PID=$!

echo "=========================================="
echo "🔥 SYSTEM ONLINE — MCP-FUSION IS LIVE 🔥"
echo "=========================================="

# ---------------------------
# 8) Trap CTRL+C and shut down cleanly
# ---------------------------
trap "echo '\n🛑 Shutting down...'; \
kill $BROKER_PID $GROK_PID $CHATGPT_PID $JUDGE_PID $LISTENER_PID $MEMORY_PID $ORCH_PID 2>/dev/null; \
echo '💤 All services stopped.'; \
exit 0" INT

# ---------------------------
# 9) Keep launcher alive so trap works
# ---------------------------
while true; do
    sleep 1
done
