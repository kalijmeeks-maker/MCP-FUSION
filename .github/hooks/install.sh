#!/usr/bin/env bash
# Install MCP-FUSION pre-commit hooks
# Usage: ./.github/hooks/install.sh

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
HOOKS_DIR="$REPO_ROOT/.github/hooks"
GIT_HOOKS_DIR="$REPO_ROOT/.git/hooks"

echo "Installing MCP-FUSION pre-commit hooks..."

# Make sure .git/hooks exists
mkdir -p "$GIT_HOOKS_DIR"

# Copy pre-commit hook
cp "$HOOKS_DIR/pre-commit" "$GIT_HOOKS_DIR/pre-commit"
chmod +x "$GIT_HOOKS_DIR/pre-commit"

echo "✅ Pre-commit hook installed at .git/hooks/pre-commit"
echo ""
echo "The hook will run on 'git commit' and check for:"
echo "  • Secret-like patterns (sk-*, xai-*, bearer tokens)"
echo "  • Architecture directive files (.github/copilot-instructions.md, ARCHITECTURE.md)"
echo "  • Ambiguous Python references in shell scripts"
echo ""
echo "To bypass (not recommended): git commit --no-verify"
echo "To uninstall: rm $GIT_HOOKS_DIR/pre-commit"
