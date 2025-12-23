"""
Grok worker

Listens on:  plasma_tasks:grok
Publishes to: plasma_results
Heartbeats:   plasma_heartbeats
"""

import os
import sys
import json
import time
import redis
import requests

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
OFFLINE = os.environ.get("FUSION_OFFLINE", "") == "1"

# IMPORTANT: XAI_API_KEY must be set in the environment or in .env
XAI_API_KEY = os.getenv("XAI_API_KEY")
XAI_MODEL = os.getenv("XAI_MODEL", "grok-2-latest")
XAI_API_URL = "https://api.x.ai/v1/chat/completions"

if not XAI_API_KEY and not OFFLINE:
    print("[GROK] ERROR: XAI_API_KEY is not set in the environment.")
    sys.exit(1)

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def send_heartbeat() -> None:
    """Send a heartbeat to let the broker know Grok worker is alive."""
    try:
        r.publish(
            "plasma_heartbeats",
            json.dumps(
                {
                    "agent": "grok",
                    "status": "alive",
                    "timestamp": time.time(),
                }
            ),
        )
    except Exception as e:
        print(f"[GROK] Heartbeat error: {e}")


def process_task(task_data: dict) -> dict:
    """Call xAI Grok for a single task or stub in offline mode."""
    try:
        prompt = task_data["prompt"]
        params = task_data.get("params", {})

        if OFFLINE:
            return {
                "task_id": task_data.get("task_id", "unknown"),
                "result": f"[OFFLINE grok] {prompt}",
                "agent": "grok",
            }

        headers = {
            "Authorization": f"Bearer {XAI_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": XAI_MODEL,
            "messages": [
                {"role": "user", "content": prompt},
            ],
            "max_tokens": params.get("max_tokens", 512),
        }

        resp = requests.post(XAI_API_URL, headers=headers, json=payload, timeout=60)
        try:
            resp.raise_for_status()
        except requests.HTTPError as http_err:
            return {
                "task_id": task_data.get("task_id", "unknown"),
                "error": f"HTTP {resp.status_code} from xAI: {http_err} | body={resp.text}",
                "agent": "grok",
            }

        data = resp.json()

        try:
            content = data["choices"][0]["message"]["content"]
        except Exception:
            return {
                "task_id": task_data.get("task_id", "unknown"),
                "error": f"Unexpected xAI response JSON: {data}",
                "agent": "grok",
            }

        return {
            "task_id": task_data.get("task_id", "unknown"),
            "result": content,
            "agent": "grok",
        }

    except Exception as e:
        return {
            "task_id": task_data.get("task_id", "unknown"),
            "error": str(e),
            "agent": "grok",
        }


def main() -> None:
    print(f"[GROK] Worker online. Listening on plasma_tasks:grok via redis://{REDIS_HOST}:{REDIS_PORT}")
    p = r.pubsub()
    p.subscribe("plasma_tasks:grok")

    send_heartbeat()

    while True:
        msg = p.get_message()
        if msg and msg["type"] == "message":
            try:
                task_data = json.loads(msg["data"])
                print(f"[GROK] Received task: {task_data.get('task_id')}")
                result = process_task(task_data)
                r.publish("plasma_results", json.dumps(result))
                print(f"[GROK] Completed task: {task_data.get('task_id')}")
            except Exception as e:
                print(f"[GROK] Fatal error in main loop: {e}")
        send_heartbeat()
        time.sleep(1)


if __name__ == "__main__":
    main()
