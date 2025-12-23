import os
import json
import time
import redis
from openai import OpenAI

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
OFFLINE = os.environ.get("FUSION_OFFLINE", "") == "1"

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def send_heartbeat():
    r.publish(
        "plasma_heartbeats",
        json.dumps(
            {
                "agent": "judge",
                "status": "alive",
                "timestamp": time.time(),
            }
        ),
    )


def judge_result(task):
    """Evaluates quality, hallucination risk, and assigns next steps."""
    if OFFLINE:
        return f"[OFFLINE judge verdict] Reviewed task: {task.get('task_id')}"

    analysis_prompt = f"""
You are the Judge Agent. Analyze the following AI output:
- Score accuracy (0-10)
- Score depth (0-10)
- Score clarity (0-10)
- Identify hallucination likelihood (low, medium, high)
- Decide if follow-up is needed
- Suggest which agent should follow if needed
- Provide a one-sentence verdict

TASK DATA:
{json.dumps(task, indent=2)}
"""
    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        messages=[{"role": "user", "content": analysis_prompt}],
        max_tokens=500,
    )
    return resp.choices[0].message.content


def main():
    print(f"[JUDGE] Online. Listening on plasma_tasks:judge via redis://{REDIS_HOST}:{REDIS_PORT}")
    p = r.pubsub()
    p.subscribe("plasma_tasks:judge")
    send_heartbeat()

    while True:
        msg = p.get_message()
        if msg and msg["type"] == "message":
            data = json.loads(msg["data"])
            verdict = judge_result(data)
            r.publish(
                "plasma_results",
                json.dumps(
                    {
                        "task_id": data["task_id"],
                        "agent": "judge",
                        "result": verdict,
                        "verdict": verdict,
                    }
                ),
            )
            print(f"[JUDGE] Scored task {data['task_id']}")
        send_heartbeat()
        time.sleep(1)


if __name__ == "__main__":
    main()
