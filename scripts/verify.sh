#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "=== MCP-FUSION VERIFY ==="
echo "Repo: $REPO_ROOT"
echo

# Prefer venv python if present; fall back to python3 on PATH (but warn)
PY=""
if [[ -x "$REPO_ROOT/.venv/bin/python" ]]; then
  PY="$REPO_ROOT/.venv/bin/python"
else
  PY="$(command -v python3 || true)"
fi

if [[ -z "$PY" ]]; then
  echo "ERROR: python3 not found on PATH and .venv/bin/python missing."
  exit 1
fi

echo "Python chosen: $PY"
"$PY" --version
echo

echo "=== Runtime discovery (sys.executable) ==="
"$PY" -c "import sys; print(sys.executable)"
echo

# Enforce runtime interpreter rule when .venv exists
if [[ -d "$REPO_ROOT/.venv" ]]; then
  echo "=== Enforcing runtime is .venv/bin/python (since .venv exists) ==="
  "$PY" -c "import sys, pathlib; exe = pathlib.Path(sys.executable).as_posix(); assert '/.venv/bin/python' in exe, f'Runtime python is not .venv/bin/python: {exe}'; print('OK: runtime python is venv-scoped')"
  echo
else
  echo "WARN: .venv directory not found. Skipping strict venv enforcement."
  echo
fi

echo "=== Dependency import checks ==="
"$PY" << 'PYEOF'
def check(mod: str):
    try:
        __import__(mod)
        print(f"OK: import {mod}")
    except Exception as e:
        raise SystemExit(f"FAIL: import {mod}: {e}")

# Keep this list short and meaningful.
check("json")
check("pathlib")

# LLM SDKs (expected for live workers). If you're still bootstrapping,
# install into the runtime interpreter shown above.
check("openai")

print("\nIf openai is missing, install into THIS runtime:\n  " + __import__("sys").executable + " -m pip install openai\n")
PYEOF

echo "
=== pip check ==="
"$PY" -m pip check || { echo "FAIL: pip check"; exit 1; }
echo

echo "
=== openai version ==="
"$PY" - << 'PYEOF2'
import openai
print(getattr(openai, "__version__", "unknown"))
PYEOF2

echo
echo "=== Verify complete: PASS ==="
