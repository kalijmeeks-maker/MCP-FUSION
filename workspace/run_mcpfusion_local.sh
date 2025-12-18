#!/bin/bash
# ==============================================================================
# Canonical Local Launcher for MCP-FUSION
#
# This script is the single, authoritative way to start the MCP-FUSION
# application stack locally. It ensures the environment is configured
# correctly and runs the main application script from the canonical
# repository location.
#
# It is designed to be called from anywhere, including from the
# master tmux launcher.
# ==============================================================================

set -euo pipefail

echo "[MCP-FUSION LAUNCHER] Starting MCP-FUSION stack locally..."

# 1. Load shared environment variables
# This sources the centralized loader script with explicit bash invocation.
bash /Users/kalimeeks/MCP-FUSION/scripts/load_env.sh

# 2. Navigate to the canonical repository root
# This ensures that all relative paths within the application resolve correctly.
cd /Users/kalimeeks/MCP-FUSION

# 3. Execute the main application script
# This runs the fusion pipeline in the foreground to capture logs.
./run_fusion.sh

echo "[MCP-FUSION LAUNCHER] MCP-FUSION stack has been terminated."

