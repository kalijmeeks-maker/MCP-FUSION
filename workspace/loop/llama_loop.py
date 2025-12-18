#!/usr/bin/env python3
import json
import os
import sys
import time

import redis

# --- Make sure we can import broker.schema --- #
# workspace_root = /Users/kalimeeks/MCP-FUSION/workspace
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from broker.schema import load_and_validate  # type: ignore

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
TASK_CHANNEL = "plasma_feed"
RESULT_CHANNEL = "plasma_results"


def publish_result(task_id: str, numbers, result: int):
    """Publish computed result back onto the bus."""
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    msg = {
        "type": "result",
        "task_id": task_id,
        "source": "llama-loop",
        "target": "grok-sim",
        "payload": {
            "result": result,
            "details": f"sum({numbers}) = {result}",
        },
        "timestamp": int(time.time()),
    }

    client.publish(RESULT_CHANNEL, json.dumps(msg))
    print(f"[LLAMA] ✔ Published result → {RESULT_CHANNEL}")


def process_message(message_data: dict):
    """'LLAMA brain' – validate type and compute."""
    msg_type = message_data.get("type")
    task_id = message_data.get("task_id")
    payload = message_data.get("payload", {})

    print(f"\n[LLAMA] Received message type={msg_type}, task_id={task_id}")
    print(f"[LLAMA] Full payload:")
    print(json.dumps(message_data, indent=2))

    if msg_type == "task" and payload.get("action") == "compute":
        numbers = payload.get("data", [])
        result = sum(numbers)
        print(f"[LLAMA] Computed result: sum({numbers}) = {result}")
        publish_result(task_id, numbers, result)
    else:
        print("[LLAMA] No compute action defined for this message.")


def main():
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    pubsub = client.pubsub()
    pubsub.subscribe(TASK_CHANNEL)

    print(f"[LLAMA] Subscribed to '{TASK_CHANNEL}'. Waiting for messages...")

    for message in pubsub.listen():
        if message["type"] != "message":
            continue

        raw_data = message["data"]

        # Schema validation
        is_valid, parsed, error = load_and_validate(raw_data)
        if not is_valid:
            print(f"[LLAMA] ❌ Invalid message rejected: {error}")
            print(f"[LLAMA] Raw data: {raw_data}")
            continue

        process_message(parsed)


if __name__ == "__main__":
    main()
