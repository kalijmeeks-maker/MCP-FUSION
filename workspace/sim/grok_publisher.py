#!/usr/bin/env python3
import json
import time
import uuid
import redis


REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
CHANNEL_NAME = "plasma_feed"


def build_task_payload():
    """Build a sample MCP-style task payload."""
    return {
        "type": "task",
        "task_id": f"task-{uuid.uuid4()}",
        "source": "grok-sim",
        "target": "llama-loop",
        "payload": {
            "action": "compute",
            "data": [1, 2, 3, 4],
            "instruction": "sum all numbers"
        },
        "timestamp": int(time.time()),
    }


def main():
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    task = build_task_payload()
    message = json.dumps(task)

    print(f"[GROK] Publishing to channel '{CHANNEL_NAME}':")
    print(json.dumps(task, indent=2))

    result = client.publish(CHANNEL_NAME, message)
    print(f"[GROK] Publish result (number of subscribers that received it): {result}")


if __name__ == "__main__":
    main()
