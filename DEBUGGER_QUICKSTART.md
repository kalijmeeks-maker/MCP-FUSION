# MCP-FUSION: Debugger-First Quickstart

## One-Button Debug Launch

**Press `F5` in VS Code** (or `Cmd+Shift+D` → Select "MCP-FUSION: Full Stack (Local)")

What happens:
1. ✅ Pre-launch validation runs (`venv-check` task)
2. ✅ Checks if `.env` exists and loads
3. ✅ Checks if `.venv/bin/python` exists
4. ✅ If OK → Launches all 6 services in debug mode
5. ❌ If missing → Clear error message with fix instructions

---

## Available Debug Configs

### Multi-Process (Compound)
- **MCP-FUSION: Full Stack (Local)** — Launches Router + 5 Workers simultaneously

### Individual Services (pick one or more)
- **Python: MCP-FUSION - Router** — `workspace/broker/router.py`
- **Python: MCP-FUSION - ChatGPT Worker** — `workspace/agents/chatgpt/worker.py`
- **Python: MCP-FUSION - Grok Worker** — `workspace/agents/grok/worker.py`
- **Python: MCP-FUSION - Judge Worker** — `workspace/agents/judge/worker.py`
- **Python: MCP-FUSION - Grok Results Listener** — `workspace/sim/grok_results_listener.py`
- **Python: MCP-FUSION - Orchestrator** — `workspace/sim/orchestrator.py`

### Generic
- **Python: Current File** — Debug any open `.py` file

---

## Terminal Commands (Fallback)

If VS Code debugging doesn't work, use these:

### Start all services (foreground):
```bash
cd /Users/kalimeeks/MCP-FUSION
./run_fusion.sh start
```

### Reload .env and restart:
```bash
./run_fusion.sh reload
```

### Stop all services:
```bash
./run_fusion.sh stop
```

### Docker-based stack (tmux + 4 panes):
```bash
cd /Users/kalimeeks/MCP-FUSION
./scripts/start_fusion_stack.sh
```

### Load .env manually:
```bash
source ./scripts/load_env.sh
```

---

## Pre-Flight Checklist

Before launching in VS Code, ensure:

- [ ] `.env` file exists at `/Users/kalimeeks/MCP-FUSION/workspace/.env`
  - Contains: `OPENAI_API_KEY`, `XAI_API_KEY`, etc.
- [ ] Virtual environment created: `workspace/.venv`
  - Create with: `cd workspace && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`
- [ ] Redis running (if Docker stack):
  - Check: `docker ps | grep mcp-fusion-redis`

---

## Debugging Tips

### Add breakpoints:
1. Click gutter next to line number
2. Debug config starts and pauses at breakpoint

### Step through code:
- **F10** = Step over
- **F11** = Step into
- **Shift+F11** = Step out
- **F5** = Continue

### View variables:
- Hover over variable name in code
- Or use Debug panel (left sidebar) → Variables tab

### View logs:
- Each service logs to its own terminal in VS Code
- Integrated terminal shows all output

### Attach to running process:
If a service crashes before you attach:
1. Start service manually: `cd workspace && python3 agents/grok/worker.py`
2. In VS Code: Run → Attach to Process
3. Find the Python process and select it

---

## Troubleshooting

### Error: `.venv not found`
```bash
cd /Users/kalimeeks/MCP-FUSION/workspace
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### Error: `.env not found`
```bash
# Create from template if it exists:
cp workspace/.env.example workspace/.env
# Edit with your API keys
```

### Error: `OPENAI_API_KEY is not set`
```bash
# Edit workspace/.env:
OPENAI_API_KEY="sk-..."  # Replace with real key
XAI_API_KEY="xai-..."    # Replace with real key
```

### Redis connection refused:
If using Docker stack, ensure Redis is running:
```bash
docker compose up -d redis
```

### Port already in use (e.g., 6379 for Redis):
```bash
# Kill process on port:
lsof -i :6379  # Find PID
kill -9 <PID>
```

---

## Architecture Recap

```
Your Code (VS Code)
    ↓
Debugger (debugpy)
    ↓
Pre-Launch Task (venv-check)
  ├─ Load .env
  ├─ Validate .venv
  └─ Continue if OK
    ↓
Router (Redis broker)
    ↓
┌─ ChatGPT Worker
├─ Grok Worker
├─ Judge Worker
├─ Grok Results Listener
└─ Orchestrator (foreground)
```

---

## Emergency Stop

If services hang:
```bash
# Kill all MCP-FUSION processes:
pkill -f "broker/router.py"
pkill -f "agents/.*worker.py"
pkill -f "sim/.*\.py"

# Or stop from VS Code: Click stop button on debug toolbar
```

---

## Next: Add Docker Debugger (Optional)

See `FIXES_SUMMARY.md` → "Priority 3" for planned Docker-based debug configs.
