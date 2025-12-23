#!/usr/bin/env bash
#
# verify.sh - Verify MCP-FUSION environment setup
#
# This script checks that all dependencies and requirements are in place
# before running the fusion stack.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "===== MCP-FUSION ENVIRONMENT VERIFICATION ====="
echo

# Check 1: Python virtual environment
echo "✓ Checking Python virtual environment..."
if [ -d ".venv" ]; then
    if [ -x ".venv/bin/python" ]; then
        PYTHON_VERSION=$(.venv/bin/python --version 2>&1)
        echo "  ✓ Virtual environment found: $PYTHON_VERSION"
    else
        echo "  ✗ Virtual environment exists but python not executable"
        exit 1
    fi
else
    echo "  ⚠ Virtual environment not found at .venv"
    echo "  Run: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
    exit 1
fi

# Check 2: Redis availability
echo
echo "✓ Checking Redis..."
if command -v redis-cli &> /dev/null; then
    if redis-cli PING &> /dev/null; then
        echo "  ✓ Redis is running and responding to PING"
    else
        echo "  ⚠ redis-cli found but Redis server not responding"
        echo "  Start Redis: redis-server (or via Docker)"
    fi
else
    echo "  ⚠ redis-cli not found in PATH"
    echo "  Install Redis or use Docker: docker compose up -d"
fi

# Check 3: Docker availability
echo
echo "✓ Checking Docker..."
if command -v docker &> /dev/null; then
    if docker info &> /dev/null; then
        echo "  ✓ Docker is available and daemon is running"
    else
        echo "  ⚠ Docker found but daemon not running"
        echo "  Start Docker daemon"
    fi
else
    echo "  ⚠ Docker not found"
    echo "  Install Docker: https://docs.docker.com/get-docker/"
fi

# Check 4: Docker Compose
echo
echo "✓ Checking Docker Compose..."
if command -v docker &> /dev/null; then
    if docker compose version &> /dev/null; then
        COMPOSE_VERSION=$(docker compose version --short 2>&1)
        echo "  ✓ Docker Compose available: $COMPOSE_VERSION"
    else
        echo "  ⚠ Docker Compose not available"
    fi
else
    echo "  ⚠ Docker not available (skipping Compose check)"
fi

# Check 5: Required directories
echo
echo "✓ Checking directory structure..."
REQUIRED_DIRS=("src" "docs" "prompts" "tests" "mcp_servers" "scripts")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✓ $dir/"
    else
        echo "  ✗ Missing: $dir/"
        exit 1
    fi
done

# Check 6: Environment file
echo
echo "✓ Checking environment configuration..."
if [ -f ".env" ]; then
    echo "  ✓ .env file exists"
else
    echo "  ⚠ .env file not found"
    echo "  Create .env with required variables (see .env.example)"
fi

# Check 7: Node dependencies (if package.json exists)
echo
echo "✓ Checking Node.js dependencies..."
if [ -f "package.json" ]; then
    if [ -d "node_modules" ]; then
        echo "  ✓ node_modules present"
    else
        echo "  ⚠ node_modules not found"
        echo "  Run: npm install"
    fi
fi

echo
echo "===== VERIFICATION COMPLETE ====="
echo "✓ Environment is ready for MCP-FUSION"
echo
