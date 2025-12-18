import json
import time
import redis

r = redis.Redis(host="localhost", port=6379, db=0)

def send_heartbeat():
    r.publish(
        "plasma_heartbeats",
        json.dumps(
            {
                "agent": "router",
                "status": "alive",
                "timestamp": time.time(),
            }
        ),
    )

p = r.pubsub()
p.subscribe("plasma_inbox")

print("[ROUTER] Listening on 'plasma_inbox'")
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
