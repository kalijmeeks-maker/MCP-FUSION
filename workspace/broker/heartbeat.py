#!/usr/bin/env python3
import argparse
import json
import time

import redis

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
HEARTBEAT_CHANNEL = "plasma_heartbeats"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", required=True, help="Agent name, e.g. grok-sim or llama-loop")
    parser.add_argument("--interval", type=int, default=10, help="Seconds between heartbeats")
    args = parser.parse_args()

    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

    print(f"[HEARTBEAT] Sending heartbeats for '{args.agent}' every {args.interval}s on '{HEARTBEAT_CHANNEL}'")

    while True:
        msg = {
            "type": "heartbeat",
            "agent": args.agent,
            "timestamp": int(time.time()),
        }
        client.publish(HEARTBEAT_CHANNEL, json.dumps(msg))
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
