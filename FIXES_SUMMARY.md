# MCP-FUSION: Debugger-First Fixes (Dec 7, 2025)

## Summary

Implemented **Fix 1–3**: Converted startup scripts and debug configs to use relative paths, added venv validation, and unified environment loading.

---

## What Was Fixed

### Fix 1: `run_fusion.sh` — Dynamic Path Resolution ✅

**Problem**: Hardcoded absolute path `/Users/kalimeeks/MCP-FUSION/workspace` broke if repo moved.

**Changes**:

- Replaced hardcoded `BASE_DIR="/Users/kalimeeks/MCP-FUSION/workspace"` with dynamic path resolution using `${BASH_SOURCE[0]}`.
- Now derives `REPO_ROOT` and `BASE_DIR` automatically, wherever the script is invoked from.
- Added improved error message for missing `.venv` with creation instructions.

**Usage**:

```bash
# Works from anywhere now:
/Users/kalimeeks/MCP-FUSION/run_fusion.sh start
cd /Users/kalimeeks/MCP-FUSION && ./run_fusion.sh start
cd /tmp && /Users/kalimeeks/MCP-FUSION/run_fusion.sh start  # ✓ All work!
```

---

### Fix 2: `scripts/load_env.sh` — Dynamic .env Path ✅

**Problem**: Hardcoded absolute path `/Users/kalimeeks/MCP-FUSION/workspace/.env` locked the script to one location.

**Changes**:

- Replaced hardcoded path with dynamic resolution from script's own directory.
- Now correctly finds `.env` regardless of where the script is called from.

**Usage**:

```bash
# From any location:
source /Users/kalimeeks/MCP-FUSION/scripts/load_env.sh
# ✓ Finds .env at /Users/kalimeeks/MCP-FUSION/workspace/.env
```

---

### Fix 3: `scripts/start_fusion_stack.sh` — Docker Paths ✅

**Problem**: Used `$HOME/MCP-FUSION` assumption, broke if repo path differed.

**Changes**:

- Replaced `REPO_PATH="$HOME/MCP-FUSION"` with dynamic resolution.
- Now discovers repo root automatically.

---

### Fix 4: `.vscode/launch.json` — Pre-Launch Validation ✅

**Problem**: If `.venv` didn't exist, debugger failed silently with cryptic errors.

**Changes**:

- Added `venv-check` task that validates both:
  - `.env` loads successfully (via `scripts/load_env.sh`)
  - `.venv/bin/python` exists and is accessible
- Added `preLaunchTask: "venv-check"` to **all 7 debug configs** (including the compound).
- If venv is missing, the debug launch now fails _loudly and helpfully_ before attempting to run.
- Added `"stopAll": true` to the Full Stack compound so stopping any config stops all 6.

**Debug Configs Now Support Pre-Launch Validation**:

- ✅ Python: Current File
- ✅ Python: MCP-FUSION - Router
- ✅ Python: MCP-FUSION - ChatGPT Worker
- ✅ Python: MCP-FUSION - Grok Worker
- ✅ Python: MCP-FUSION - Judge Worker
- ✅ Python: MCP-FUSION - Grok Results Listener
- ✅ Python: MCP-FUSION - Orchestrator

---

## File Changes

| File                            | Change                                | Impact                       |
| ------------------------------- | ------------------------------------- | ---------------------------- |
| `run_fusion.sh`                 | Hardcoded → Dynamic paths             | ✅ Works from any directory  |
| `scripts/load_env.sh`           | Hardcoded → Dynamic paths             | ✅ Relocatable env loading   |
| `scripts/start_fusion_stack.sh` | `$HOME` → Dynamic paths               | ✅ Docker stack portable     |
| `.vscode/launch.json`           | Added venv-check task + preLaunchTask | ✅ Debugger-first validation |

---

## How to Verify Everything Works

### 1. Test scripts from any directory:

```bash
cd /tmp
/Users/kalimeeks/MCP-FUSION/run_fusion.sh start  # Should work
# (Will fail on missing API keys, but script paths will be correct)
```

### 2. Test env loading:

```bash
cd /Users/kalimeeks/MCP-FUSION
source scripts/load_env.sh
echo $PYTHONPATH  # Should show environment loaded
```

### 3. Test venv-check task:

```bash
cd /Users/kalimeeks/MCP-FUSION
bash -c "scripts/load_env.sh && test -f workspace/.venv/bin/python && echo '[VENV] Ready'"
```

### 4. Launch a debug config in VS Code:

- Press `F5` or `Cmd+Shift+D` → Select `MCP-FUSION: Full Stack (Local)`
- Debugger will:
  - Run `venv-check` pre-launch task
  - Validate `.env` and `.venv` exist
  - If missing → Fail with clear error message
  - If present → Launch all 6 processes

---

## Design Philosophy

### Debugger-First Principles Applied:

1. **Pre-launch validation** — Catch env issues _before_ launching, not mid-execution.
2. **Relative paths** — Scripts work whether repo is at `/Users/kalimeeks/MCP-FUSION` or anywhere else.
3. **Fail loudly** — Better to exit with a clear message than silently hang.
4. **Single source of truth** — `run_fusion.sh` and `.vscode/launch.json` use the same venv path.

---

## Next Steps (Optional)

### Priority 3 (Nice-to-have):

- Add Docker-based debug configs that use `docker exec` for containerized debugging.
- Create a `Makefile` or `just` file for common workflows (start, stop, reload, test).
- Add health-check script to verify Redis and worker connectivity before launching.

---

## Questions?

All scripts use `set -e` so any errors halt execution. Check the terminal output for details.
