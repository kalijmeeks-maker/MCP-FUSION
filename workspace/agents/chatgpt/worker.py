import os
import json
import time
import redis
from openai import OpenAI

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o")
OFFLINE = os.environ.get("FUSION_OFFLINE", "") == "1"

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def send_heartbeat():
    r.publish(
        "plasma_heartbeats",
        json.dumps(
            {
                "agent": "chatgpt",
                "status": "alive",
                "timestamp": time.time(),
            }
        ),
    )


p = r.pubsub()
p.subscribe("plasma_tasks:chatgpt")

print(f"[CHATGPT] Worker online. Listening on plasma_tasks:chatgpt via redis://{REDIS_HOST}:{REDIS_PORT}")

while True:
    msg = p.get_message()
    if msg and msg["type"] == "message":
        try:
            task = json.loads(msg["data"])
            prompt = task["prompt"]
            params = task.get("params", {})

            if OFFLINE:
                result = f"[OFFLINE chatgpt] {prompt}"
            else:
                response = client.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=params.get("max_tokens", 200),
                )
                result = response.choices[0].message.content

            r.publish(
                "plasma_results",
                json.dumps(
                    {
                        "task_id": task["task_id"],
                        "result": result,
                        "agent": "chatgpt",
                    }
                ),
            )

            print(f"[CHATGPT] Completed task: {task['task_id']}")

        except Exception as e:
            r.publish(
                "plasma_results",
                json.dumps(
                    {
                        "task_id": task.get("task_id"),
                        "error": str(e),
                        "agent": "chatgpt",
                    }
                ),
            )
    send_heartbeat()
    time.sleep(1)
