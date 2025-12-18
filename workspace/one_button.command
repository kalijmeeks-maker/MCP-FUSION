#!/bin/zsh
echo "=== MCP Fusion v0.5A Launcher ==="

SCRIPT_DIR="/Users/kalimeeks/MCP-FUSION/workspace"
cd "$SCRIPT_DIR" || { echo "ERROR: cannot cd to $SCRIPT_DIR"; exit 1; }

# load env
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
else
  echo "ERROR: .env not found"; exit 1
fi

# sanity
if [ -z "$OPENAI_API_KEY" ]; then
  echo "ERROR: Missing OPENAI_API_KEY in .env"; exit 1;
fi
if [ -z "$XAI_API_KEY" ]; then
  echo "ERROR: Missing XAI_API_KEY in .env"; exit 1;
fi

# launch
echo "Launching Fusion CLI..."
python3 fusion_cli.py "$@"
