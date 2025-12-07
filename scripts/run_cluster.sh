#!/bin/bash

cd /Users/kalimeeks/MCP-FUSION/workspace
source .venv/bin/activate

echo "[MCP-FUSION] Starting AI cluster..."

python3 loop/llama_loop.py & \
echo " - LLaMA Loop online"

python3 sim/grok_results_listener.py & \
echo " - Grok Listener online"

python3 broker/heartbeat.py --agent llama-loop --interval 5 & \
echo " - Heartbeat (llama-loop) online"

python3 broker/heartbeat.py --agent grok-sim --interval 7 & \
echo " - Heartbeat (grok-sim) online"

python3 broker/heartbeat_monitor.py & \
echo " - Heartbeat Monitor online"

echo "🔥 MCP-FUSION CLUSTER ACTIVE"
