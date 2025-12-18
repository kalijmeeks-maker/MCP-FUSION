#!/usr/bin/env bash
set -euo pipefail
cd /Users/kalimeeks/MCP-FUSION

PY="/Users/kalimeeks/MCP-FUSION/.venv/bin/python"
echo "== PLASMA PEEK (last 3) =="

"$PY" << 'PYEOF'
import os, json
import redis

host = os.environ.get("REDIS_HOST", "localhost")
port = int(os.environ.get("REDIS_PORT", "6379"))
r = redis.Redis(host=host, port=port, decode_responses=True)

items = r.lrange("plasma_results", -3, -1)
print(f"redis://{host}:{port}  plasma_results last3={len(items)}")
for i, raw in enumerate(items, 1):
    try:
        obj = json.loads(raw)
        print(f"\n--- item {i} (json) ---")
        print(json.dumps(obj, indent=2)[:2000])
    except Exception:
        print(f"\n--- item {i} (raw) ---")
        print(raw[:2000])
PYEOF
