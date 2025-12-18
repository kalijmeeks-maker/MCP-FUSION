import os
import json
import time
import redis
from openai import OpenAI

# Redis
r = redis.Redis(host='localhost', port=6379, db=0)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def send_heartbeat():
    r.publish("plasma_heartbeats", json.dumps({
        "agent": "chatgpt",
        "status": "alive",
        "timestamp": time.time(),
    }))

p = r.pubsub()
p.subscribe("plasma_tasks:chatgpt")

print("[CHATGPT] Worker online. Listening on plasma_tasks:chatgpt")

while True:
    msg = p.get_message()
    if msg and msg["type"] == "message":
        try:
            task = json.loads(msg["data"])
            prompt = task["prompt"]
            params = task.get("params", {})

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=params.get("max_tokens", 200)
            )

            result = response.choices[0].message.content

            r.publish("plasma_results", json.dumps({
                "task_id": task["task_id"],
                "result": result,
                "agent": "chatgpt",
            }))

            print(f"[CHATGPT] Completed task: {task['task_id']}")

        except Exception as e:
            r.publish("plasma_results", json.dumps({
                "task_id": task.get("task_id"),
                "error": str(e),
                "agent": "chatgpt",
            }))
    send_heartbeat()
    time.sleep(1)
