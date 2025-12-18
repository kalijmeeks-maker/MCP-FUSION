#!/usr/bin/env python3
import json
import time
from collections import defaultdict

import redis

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
HEARTBEAT_CHANNEL = "plasma_heartbeats"
STALE_AFTER = 30  # seconds


def main():
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    pubsub = client.pubsub()
    pubsub.subscribe(HEARTBEAT_CHANNEL)

    last_seen = defaultdict(lambda: 0)

    print(f"[MONITOR] Listening for heartbeats on '{HEARTBEAT_CHANNEL}'")

    last_status_print = 0

    for message in pubsub.listen():
        if message["type"] != "message":
            continue

        raw = message["data"]
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            print(f"[MONITOR] Invalid heartbeat JSON: {raw}")
            continue

        agent = data.get("agent", "unknown")
        ts = data.get("timestamp", 0)
        last_seen[agent] = ts

        now = time.time()
        # Periodically print status
        if now - last_status_print >= 10:
            print("\n[MONITOR] Agent status:")
            for a, t in last_seen.items():
                age = now - t
                state = "ONLINE" if age <= STALE_AFTER else "STALE/OFFLINE?"
                print(f"  - {a:15s} last={int(age):3d}s ago  → {state}")
            last_status_print = now
