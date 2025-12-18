#!/usr/bin/env python3
import json

import redis

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
RESULT_CHANNEL = "plasma_results"


def main():
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    pubsub = client.pubsub()
    pubsub.subscribe(RESULT_CHANNEL)

    print(f"[GROK] Listening for results on '{RESULT_CHANNEL}'...")

    for message in pubsub.listen():
        if message["type"] != "message":
            continue

        raw = message["data"]
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            print(f"[GROK] ❌ Invalid JSON on {RESULT_CHANNEL}: {raw}")
            continue

        print("\n[GROK] ✔ RESULT RECEIVED:")
        print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
