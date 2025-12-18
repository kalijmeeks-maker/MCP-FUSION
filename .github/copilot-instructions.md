# MCP-FUSION Copilot Architecture Directives

> **Critical Context for AI Assistants**  
> Read this document carefully before making recommendations about Python dependencies, runtime environments, or debugging import errors.

---

## ⚡ THE RUNTIME (TL;DR)

**The Fusion runtime Python is explicitly isolated in:**
```
/Users/kalimeeks/MCP-FUSION/.venv/bin/python
```

All LLM SDKs and dependencies **must** be installed into **this exact interpreter**:
```bash
/Users/kalimeeks/MCP-FUSION/.venv/bin/python -m pip install openai xai redis
```

**Never guess.** If you see import errors, first check `sys.executable` inside a worker—it will point to this path.

---

## System Architecture Overview

MCP-FUSION is a Python-based multi-agent orchestration system with **two distinct execution layers** that must be understood separately:

### 1️⃣ Launcher Layer (Control Plane)

- **File**: `start-fusion-stack.command` / `one_button.command`
- **Language**: `zsh` / `bash`
- **Purpose**:
  - Set environment variables
  - Dispatch pipeline execution
  - Orchestrate Docker services
- **Interpreter**: `/bin/zsh` (by design)
- **⚠️ CRITICAL**: This is **NOT** a Python runtime
- **⚠️ NEVER** install Python packages into this shell environment

### 2️⃣ Runtime Layer (Execution Plane)

- **Language**: Python
- **Components**:
  - `planner` worker
  - `critic` worker
  - `coordinator` worker
  - Core modules (`core.llm_clients`, `core.config`, etc.)
- **Purpose**: Execute AI agent logic
- **Interpreter**: Whatever `sys.executable` returns inside the runtime
- **Dependencies Required**:
  - `openai`
  - `xai`
  - `redis`
  - `anthropic` (optional)
  - Future LLM SDKs

**This is where all Python packages must be installed.**

---

## Historical Failure Mode (MUST AVOID)

### ❌ Symptoms Observed

```
No module named 'core.llm_clients'
No module named 'openai'
Coordinator falling back to mock output
```

### ❌ Root Cause (Incorrect Assumptions)

AI assistants mistakenly:
- Treated `.command` shebang as a Python interpreter
- Attempted to run `pip` against `/bin/zsh`
- Inferred Python paths from launcher scripts instead of runtime
- Installed dependencies in the **wrong interpreter**

### ❌ Why This is Architecturally Wrong

The launcher (control plane) is a **shell script** that spawns Python processes.  
Python workers run in a **separate runtime environment**.  
These are **not the same interpreter**.

---

## ✅ Correct Diagnostic Method (MANDATORY)

When debugging import errors or installing dependencies:

### Step 1: Identify Runtime Python

**Run inside the Fusion worker runtime** (not the launcher):

```python
import sys
print(sys.executable)
```

**Example output**:
```
/usr/local/bin/python3.11
```

### Step 2: Install Dependencies Using That Exact Python

```bash
/usr/local/bin/python3.11 -m pip install openai xai redis
```

### Step 3: Verify Import

```python
import openai
import xai
print("Success!")
```

### ❌ NEVER Do This

```bash
# WRONG - installing into the launcher shell
pip install openai

# WRONG - guessing the Python path
/usr/bin/python3 -m pip install openai

# WRONG - assuming system Python
python3 -m pip install openai
```

**Always use the exact path from `sys.executable`.**

---

## Verified Resolution Pattern

The following workflow has been proven to resolve import errors:

1. **Detect** runtime Python via `sys.executable`
2. **Install** dependencies into that exact interpreter
3. **Verify** imports work inside the runtime
4. **Re-run** the pipeline
5. **Confirm** no more mock fallback errors

---

## Directives for AI Assistants

When working with MCP-FUSION, you MUST:

✅ **DO**:
- Treat `.command` files as **control-plane only**
- Treat Python workers as **execution-plane**
- Always confirm runtime Python explicitly using `sys.executable`
- Install LLM SDK dependencies into the **runtime interpreter**
- If an LLM client import fails, assume **dependency placement error first**, not missing code

❌ **DO NOT**:
- Recommend installing Python packages into shell interpreters
- Infer Python paths from launcher scripts
- Assume system Python is the runtime Python
- Treat shell script shebangs as Python interpreters
- Guess package installation locations

---

## Quick Reference

| Component | Layer | Language | Install Deps Here? |
|-----------|-------|----------|-------------------|
| `start-fusion-stack.command` | Control Plane | zsh/bash | ❌ NO |
| `one_button.command` | Control Plane | zsh/bash | ❌ NO |
| `scripts/*.sh` | Control Plane | bash | ❌ NO |
| Fusion workers | Execution Plane | Python | ✅ YES |
| `core/*` modules | Execution Plane | Python | ✅ YES |

---

## Acknowledgment Required

Before making recommendations about:
- Python dependencies
- Import errors
- Package installation
- Runtime environments

**You MUST acknowledge this architecture** and explain your understanding of the launcher vs. runtime distinction.

Failure to follow these directives will result in incorrect guidance and repeated failures.

---

*Last Updated: December 17, 2025*  
*Document Owner: MCP-FUSION Architecture Team*
