# MCP-FUSION REPL Quick Start

Complete guide to using the MCP-FUSION Interactive REPL (Read-Eval-Print Loop).

## What is the Fusion REPL?

The Fusion REPL is an interactive command-line interface that lets you:

- Submit tasks to the MCP-FUSION orchestration system
- Get real-time responses from multiple AI models
- Test multi-model fusion workflows
- Debug and experiment with the system

## Prerequisites

### Required

1. **Python 3.8+** with venv
2. **Redis Server** running locally or via Docker
3. **MCP-FUSION repository** cloned

### Optional

- Docker & Docker Compose (alternative to local Redis)

## Setup

### 1. Create Python Virtual Environment

```bash
cd /path/to/MCP-FUSION
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Redis

**Option A: Local Redis**

```bash
redis-server
```

**Option B: Docker**

```bash
docker compose up -d
```

### 4. Verify Environment

```bash
./scripts/verify.sh
```

Should show all green checkmarks ✓

## Quick Start

### Launch the REPL

```bash
./scripts/start_fusion_repl.sh
```

This will:

1. ✓ Verify your environment
2. ✓ Check Redis connectivity
3. ✓ Start the coordinator worker
4. ✓ Run a smoke test
5. ✓ Launch the interactive REPL

### First Command

At the `fusion>` prompt, type:

```
fusion> What is MCP-FUSION?
```

Press Enter and wait for the response.

## Usage Examples

### Simple Prompt

```
fusion> Explain quantum computing in simple terms
```

### Structured Request

```
fusion> Analyze the sentiment of: "I love this product!"
```

### Multi-Model Comparison

```
fusion> Compare approaches: recursive vs iterative algorithms
```

### Code Generation

```
fusion> Write a Python function to validate email addresses
```

## REPL Commands

### Basic Usage

```
fusion> <your prompt here>    # Submit a task
Ctrl+C                         # Exit REPL
```

### Environment Variables

Customize behavior with environment variables:

```bash
# Custom queue names
export FUSION_TASK_LIST=my_tasks
export FUSION_RESULT_LIST=my_results

# Longer wait time for results
export FUSION_WAIT_S=2.0

# Launch REPL
./scripts/start_fusion_repl.sh
```

## Architecture

```
┌─────────────┐
│   User      │
│  (REPL)     │
└──────┬──────┘
       │ task
       ▼
┌─────────────────┐
│  Redis Queue    │
│ fusion_tasks    │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ Coordinator Worker  │
│  (Background)       │
└────────┬────────────┘
         │ result
         ▼
┌─────────────────┐
│  Redis Queue    │
│ plasma_results  │
└────────┬────────┘
         │
         ▼
┌─────────────┐
│   User      │
│  (REPL)     │
└─────────────┘
```

## Manual Operations

### Start Coordinator Manually

```bash
# Foreground (see output)
python -m workspace.workers.coordinator_worker

# Background
nohup python -m workspace.workers.coordinator_worker > coordinator.log 2>&1 &
```

### Submit Tasks Manually

```bash
# Via redis-cli
redis-cli LPUSH fusion_tasks '{"task":"Hello world","constraints":{}}'

# Via Python
python -c '
import redis, json
r = redis.Redis()
r.lpush("fusion_tasks", json.dumps({"task": "Test", "constraints": {}}))
'
```

### Check Results

```bash
# Get latest result
redis-cli LRANGE plasma_results 0 0

# Get all results
redis-cli LRANGE plasma_results 0 -1

# Monitor in real-time
redis-cli MONITOR
```

### Stop Coordinator

```bash
# Find process
ps aux | grep coordinator_worker

# Kill by PID
kill <PID>

# Or kill all Python processes (use with caution!)
pkill -f coordinator_worker
```

## Troubleshooting

### Redis Connection Error

```
ERROR: Redis not responding
```

**Solution:**

```bash
# Check if Redis is running
redis-cli PING

# If not, start it
redis-server
# or
docker compose up -d
```

### Coordinator Not Starting

```
ERROR: Coordinator failed to start
```

**Solution:**

```bash
# Check the log
tail -f workspace/memory/coordinator_*.log

# Common issues:
# - Redis not running
# - Port 6379 blocked
# - Missing dependencies (run: pip install -r requirements.txt)
```

### No Results Appearing

```
⚠ No results yet in plasma_results
```

**Solution:**

```bash
# Increase wait time
export FUSION_WAIT_S=3.0
./scripts/start_fusion_repl.sh

# Or check if coordinator is running
ps aux | grep coordinator_worker

# Check coordinator log for errors
tail -f workspace/memory/coordinator_*.log
```

### Python Module Not Found

```
ModuleNotFoundError: No module named 'redis'
```

**Solution:**

```bash
# Make sure you're in venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Advanced Usage

### Custom Task Format

Edit `scripts/fusion_repl.py` to customize the task payload:

```python
payload = {
    "task": task,
    "constraints": {
        "format": "json",
        "no_markdown": True,
        "max_tokens": 2000,        # Add custom constraints
        "temperature": 0.7
    },
    "metadata": {
        "user": "your_name",
        "session_id": "abc123"
    }
}
```

### Multiple Coordinators

Run multiple coordinator workers for load balancing:

```bash
# Terminal 1
python -m workspace.workers.coordinator_worker

# Terminal 2
python -m workspace.workers.coordinator_worker

# Both will process tasks from the same queue
```

### Logging Configuration

Set log level:

```bash
export LOG_LEVEL=DEBUG
python -m workspace.workers.coordinator_worker
```

## Integration with AI Models

The coordinator worker is designed to integrate with multiple AI models. To add model support:

1. Edit `workspace/workers/coordinator_worker.py`
2. Add model API clients in `process_task()` method
3. Implement fusion logic to merge responses

Example structure:

```python
def process_task(self, task_data):
    task = task_data["task"]

    # Query multiple models
    gpt_response = call_gpt(task)
    claude_response = call_claude(task)
    deepseek_response = call_deepseek(task)

    # Merge with Judge Agent logic
    merged_result = merge_responses([
        gpt_response,
        claude_response,
        deepseek_response
    ])

    return merged_result
```

## Next Steps

1. **Add Model Integration**: Connect actual AI model APIs
2. **Implement Fusion Logic**: Build Judge Agent for response merging
3. **Add MCP Servers**: Integrate Puppeteer, Filesystem, etc.
4. **Build Web UI**: Create a web-based interface
5. **Add Authentication**: Secure the system with auth

## Resources

- [Main README](../README.md)
- [Workspace Documentation](../workspace/README.md)
- [MCP Servers](../mcp_servers/README.md)
- [Fusion Agent Prompts](../prompts/README.md)

---

**Need Help?** Create an issue using the Session template: `.github/ISSUE_TEMPLATE/session.yml`
