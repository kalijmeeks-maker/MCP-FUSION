# MCP-FUSION Architecture

**Master Document for System Design, Layer Separation, and Runtime Dependencies**

---

## Executive Summary

MCP-FUSION is a **multi-layered, multi-agent orchestration system** designed with strict separation between the **control plane** (shell launcher) and the **execution plane** (Python runtime).

This document ensures all contributors, developers, and AI assistants understand:
1. Why the architecture is split this way
2. How each layer works independently
3. Where dependencies belong
4. How to debug common failures

---

## System Architecture (Non-Negotiable)

### Layer 1: Control Plane (Launcher)

**Files**:
- `start-fusion-stack.command`
- `scripts/*.sh`
- `run_fusion.sh`

**Technology**: Shell scripting (`zsh`, `bash`)

**Purpose**:
- Set environment variables (`PATH`, `PYTHON_VERSION`, etc.)
- Initialize Docker containers (Redis, fusion worker services)
- Start and manage tmux session(s)
- Dispatch worker processes to the Python runtime
- Monitor and orchestrate service health

**Interpreter**: `/bin/zsh` or `/bin/bash`

**Dependency Installation**: ❌ **NEVER install Python packages here**

**Why**: The launcher is a **control script**, not an execution environment. It spawns Python workers that run in **separate, isolated interpreters**. Installing packages into the shell environment will not make them available to Python workers.

---

### Layer 2: Execution Plane (Runtime)

**Components**:
- `workers/planner/`
- `workers/critic/`
- `workers/coordinator/`
- `core/` (shared modules)
- `core/llm_clients/`
- `core/config/`

**Technology**: Python

**Purpose**:
- Execute AI agent logic
- Interact with LLM APIs (OpenAI, Anthropic, XAI, etc.)
- Orchestrate agent workflows
- Maintain shared state via Redis broker

**Interpreter**: Whatever `sys.executable` returns inside the Python worker process.

**Example**:
```python
import sys
print(sys.executable)
# Output: /usr/local/bin/python3.11
# (or /opt/miniconda3/bin/python3, /home/user/.venv/bin/python, etc.)
```

**Dependency Installation**: ✅ **Install ALL Python packages here**

**Required Dependencies**:
- `openai` (OpenAI API client)
- `xai` (XAI API client, if using Grok)
- `anthropic` (Anthropic Claude API client, optional)
- `redis` (Redis broker interaction)
- `pydantic` (configuration validation)
- `tenacity` (retry logic for LLM calls)
- Other worker-specific deps

---

## Why Layer Separation Matters

### Problem: Single Environment Confusion

If we treated the launcher as the Python runtime:

```bash
# Launcher script (zsh)
#!/bin/zsh
pip install openai  # ❌ Installs into shell environment, not workers

# Python worker (separate process)
import openai  # ❌ NOT FOUND - openai in shell, not in worker's Python
```

### Solution: Explicit Layer Separation

```bash
# Launcher script (zsh)
#!/bin/zsh
# Only orchestration logic here

# Worker startup identifies Python
python3 -c "import sys; print(sys.executable)"
# Output: /usr/local/bin/python3.11

# Install into that exact Python
/usr/local/bin/python3.11 -m pip install openai

# Python worker (separate process)
import openai  # ✅ FOUND - openai in worker's Python
```

---

## Critical Failure Mode: Import Errors

### ❌ Symptoms Observed (Repeated)

```
No module named 'core.llm_clients'
No module named 'openai'
Coordinator falling back to mock output
```

### ❌ Root Cause Analysis

1. **Wrong Assumption**: Packages were installed into launcher shell, not runtime Python
2. **Why It Failed**: Launcher and runtime are separate interpreters
3. **Detection Failure**: No explicit verification of `sys.executable` inside workers
4. **Result**: Workers failed silently and fell back to mock coordinator

### ✅ Correct Diagnostic Path

When you see import errors:

**Step 1: Never assume.** Print the runtime Python:

```python
# Inside a worker
import sys
print(f"Worker running on: {sys.executable}")
```

**Step 2: Install into that exact Python:**

```bash
/path/from/step/1 -m pip install openai xai redis
```

**Step 3: Verify locally:**

```python
# Run inside a worker context
import openai
import xai
import redis
print("All imports successful!")
```

**Step 4: Re-run pipeline:**

```bash
./start-fusion-stack.command
```

---

## Dependency Management Best Practices

### ✅ Correct: Install into Runtime Python

```bash
# Identify runtime
python_bin="/usr/local/bin/python3.11"

# Install dependencies
$python_bin -m pip install openai xai redis anthropic

# Verify
$python_bin -c "import openai, xai; print('Success!')"
```

### ❌ Incorrect: Install into Shell

```bash
# Do NOT do this
pip install openai

# Do NOT do this
/usr/bin/python -m pip install openai

# Do NOT do this
python3 -m pip install openai
```

### ❌ Incorrect: Assume System Python

```bash
# Do NOT assume system Python is the worker Python
which python3
# May return /usr/local/bin/python3 or /opt/homebrew/bin/python3
# But worker might run /usr/bin/python3 or /opt/miniconda3/bin/python3

# Always verify explicitly
import sys; print(sys.executable)
```

---

## Docker Environment (Advanced)

If running workers inside Docker containers:

```dockerfile
# Inside Dockerfile
RUN /opt/python/python3.11/bin/python -m pip install openai xai redis

# Verify
RUN /opt/python/python3.11/bin/python -c "import openai; print('OK')"
```

The same principle applies: **install into the exact Python that will run the worker**.

---

## Debugging Checklist

When debugging import or runtime errors, follow this checklist:

### 1. Confirm Runtime Python

```python
# In worker code
import sys
print(f"sys.executable = {sys.executable}")
print(f"sys.path = {sys.path}")
```

### 2. Verify Dependency Installation

```bash
# Using the Python from step 1
<runtime_python> -m pip list | grep openai
<runtime_python> -m pip list | grep xai
```

### 3. Test Import in Isolation

```bash
# Direct test
<runtime_python> -c "import openai; print(openai.__version__)"
```

### 4. Check Environment Variables

```python
# Inside worker
import os
print(os.environ.get("PYTHON_PATH"))
print(os.environ.get("PATH"))
```

### 5. Confirm No Version Conflicts

```bash
# Check for multiple Python installations
which python python3 python3.11
ls -la /usr/bin/python* /usr/local/bin/python* ~/.venv/bin/python*
```

---

## Rules for AI Assistants (Copilot, ChatGPT, etc.)

**Read `.github/copilot-instructions.md` for the full directive.**

In brief:

✅ **DO**:
1. Treat `.command` files as control-plane only
2. Treat Python workers as execution-plane
3. Always confirm runtime Python explicitly: `import sys; print(sys.executable)`
4. Install packages into runtime Python, not the shell
5. If import fails, assume wrong installation location first, not missing code

❌ **DO NOT**:
1. Recommend installing packages into shell interpreters
2. Infer Python paths from launcher scripts
3. Assume system Python is the runtime Python
4. Guess package installation locations
5. Treat shell script shebangs as Python interpreters

---

## Quick Reference: Layer Responsibilities

| Task | Layer | Example |
|------|-------|---------|
| Set environment variables | Control Plane | `export REDIS_URL=...` |
| Start Docker services | Control Plane | `docker-compose up` |
| Install Python packages | **Execution Plane** | `python3 -m pip install openai` |
| Import LLM clients | Execution Plane | `import openai` |
| Handle retries/timeouts | Execution Plane | `from tenacity import retry` |
| Monitor worker health | Control Plane | `docker ps`, `tmux list-panes` |
| Parse agent responses | Execution Plane | JSON response parsing |
| Log to Redis | Execution Plane | `redis.lpush("logs", ...)` |

---

## Folder Structure

```
/Users/kalimeeks/MCP-FUSION/
├── .github/
│   └── copilot-instructions.md       # AI Assistant Guidelines
├── scripts/
│   ├── start_fusion_stack.sh          # Main launcher
│   └── gemini_sync.sh                 # Gemini CLI helper
├── workers/
│   ├── planner/
│   │   └── __main__.py                # Planner worker (execution plane)
│   ├── critic/
│   │   └── __main__.py                # Critic worker (execution plane)
│   └── coordinator/
│       └── __main__.py                # Coordinator worker (execution plane)
├── core/
│   ├── llm_clients/                   # LLM integration (execution plane)
│   ├── config.py                      # Config management (execution plane)
│   └── redis_broker.py                # Redis interaction (execution plane)
├── start-fusion-stack.command         # macOS launcher (control plane)
├── run_fusion.sh                      # Bash launcher (control plane)
├── ARCHITECTURE.md                    # This file
└── README.md                          # Quick start guide
```

---

## Environment Variables

**Set by Control Plane**:
```bash
export REDIS_URL=redis://localhost:6379
export PYTHONPATH=/Users/kalimeeks/MCP-FUSION
export OPENAI_API_KEY=your_key_here
export XAI_API_KEY=your_key_here
```

**Read by Execution Plane**:
```python
import os
redis_url = os.environ["REDIS_URL"]
api_key = os.environ["OPENAI_API_KEY"]  # Set in launcher or .env
```

---

## Troubleshooting Guide

### Problem: `No module named 'openai'`

**Check**:
```python
import sys
print(sys.executable)
# Then verify openai is installed in that Python
```

**Fix**:
```bash
<runtime_python> -m pip install openai
```

### Problem: `No module named 'core.llm_clients'`

**Check**:
```python
import sys
print(sys.path)
# Verify /Users/kalimeeks/MCP-FUSION is in sys.path
```

**Fix**:
```bash
# In launcher or worker startup
export PYTHONPATH=/Users/kalimeeks/MCP-FUSION:$PYTHONPATH
```

### Problem: Workers fall back to mock coordinator

**Check**: Monitor logs for import errors during startup. See debugging checklist above.

### Problem: Environment variable not found

**Check**:
```python
import os
print(os.environ.get("REDIS_URL"))
```

**Fix**: Ensure launcher sets it before spawning workers.

---

## Next Steps

1. **New to MCP-FUSION?** Read [README.md](README.md) for quick-start instructions.
2. **Debugging an issue?** Follow the [Debugging Checklist](#debugging-checklist) above.
3. **Contributing code?** Ensure all Python dependencies are in `requirements.txt` (for execution plane).
4. **Working with AI Assistants?** Point them to [.github/copilot-instructions.md](.github/copilot-instructions.md).

---

**Last Updated**: December 17, 2025  
**Document Owner**: MCP-FUSION Architecture Team  
**Version**: 1.0
