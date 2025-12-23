# Workspace Directory

This directory contains the runtime workspace for the MCP-FUSION system.

## Structure

```
/workspace
  /workers         - Background workers for task processing
  /memory          - Logs and persistent state
  __init__.py      - Package initialization
```

## Workers

### coordinator_worker.py

The coordinator worker manages the task queue and orchestrates multi-model fusion workflows.

**Responsibilities:**

- Listen for tasks on the `fusion_tasks` Redis queue
- Coordinate execution across multiple AI models
- Aggregate and merge results
- Publish results to the `plasma_results` Redis queue

**Core API:**

The `handle_task(task: str)` function is the main entry point for task processing:

```python
from workspace.workers.coordinator_worker import handle_task

# Process a task
result = handle_task("Explain quantum computing")

# Returns:
# {
#     "task": "Explain quantum computing",
#     "status": "processed",
#     "response": "Processed: Explain quantum computing",
#     "length": 26,
#     "timestamp": 1703345678.123
# }
```

This function can be:
- Called directly by custom coordinators
- Imported by REPL interfaces
- Extended with multi-model fusion logic

**Running:**

```bash
# Start coordinator in background
python -m workspace.workers.coordinator_worker

# Or use the launcher script
./scripts/start_fusion_repl.sh
```

**Configuration:**

Set these environment variables:

- `FUSION_TASK_LIST` - Redis list for tasks (default: `fusion_tasks`)
- `FUSION_RESULT_LIST` - Redis list for results (default: `plasma_results`)
- `REDIS_HOST` - Redis host (default: `localhost`)
- `REDIS_PORT` - Redis port (default: `6379`)
- `FUSION_POLL_INTERVAL` - Polling interval in seconds (default: `0.5`)

## Memory

The `/memory` directory stores:

- Coordinator logs
- Task execution history
- Model response caches
- Session state

Logs are automatically rotated with timestamps:

```
workspace/memory/coordinator_20241223_120000.log
```

## Development

### Adding a New Worker

1. Create a new Python module in `/workers`
2. Implement the worker class with a `run()` method
3. Add proper logging and error handling
4. Update this README with worker documentation

### Testing Workers

```bash
# Test coordinator locally
python -m workspace.workers.coordinator_worker

# Monitor Redis queues
redis-cli MONITOR

# Submit test task
redis-cli LPUSH fusion_tasks '{"task":"test","constraints":{}}'

# Check results
redis-cli LRANGE plasma_results 0 -1
```

## Redis Queue Protocol

### Task Format

```json
{
  "task": "Your prompt or request here",
  "constraints": {
    "format": "json",
    "no_markdown": true,
    "max_tokens": 1000
  }
}
```

### Result Format

```json
{
  "status": "processed",
  "task": "Original task",
  "response": "Model response",
  "models_used": ["gpt-4", "claude-3"],
  "timestamp": 1703345678.123
}
```

## Dependencies

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Key dependencies:

- `redis` - Redis client for Python

## Integration with MCP Servers

Workers can integrate with MCP servers defined in `/mcp_servers`:

- Puppeteer for browser automation
- Filesystem for file operations
- Git for repository management
- GGWave for audio communication
- Notion for API integration

See `/mcp_servers/README.md` for MCP server documentation.

---

For more information, see the main [README.md](../README.md) and [docs/context.md](../docs/context.md).
