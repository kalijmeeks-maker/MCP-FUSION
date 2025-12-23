import json
import os
import time
import redis

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
HEARTBEAT_KEY = "broker_heartbeat"
HEARTBEAT_CHANNEL = "plasma_heartbeats"

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def send_heartbeat() -> None:
    payload = {
        "agent": "router",
        "status": "alive",
        "timestamp": time.time(),
    }
    r.publish(HEARTBEAT_CHANNEL, json.dumps(payload))
    r.set(HEARTBEAT_KEY, payload["timestamp"])


p = r.pubsub()
p.subscribe("plasma_inbox")

print(f"[ROUTER] Listening on 'plasma_inbox' via redis://{REDIS_HOST}:{REDIS_PORT}")
send_heartbeat()

while True:
    msg = p.get_message()
    if msg and msg["type"] == "message":
        try:
            task = json.loads(msg["data"])
            target = task.get("target")

            if not target:
                print("[ROUTER] ❌ Task missing 'target' field, dropping.")
                continue

            out_channel = f"plasma_tasks:{target}"
            r.publish(out_channel, json.dumps(task))
            print(f"[ROUTER] Routed {task.get('task_id')} → {out_channel}")

        except json.JSONDecodeError:
            print("[ROUTER] ❌ Invalid JSON in plasma_inbox, dropping.")

    send_heartbeat()
    time.sleep(1)
