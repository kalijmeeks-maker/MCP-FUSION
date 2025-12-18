import sys
import json
import time
import uuid
import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

def main():
    """
    Usage examples:
      python3 sim/planner_free.py chatgpt "What is the capital of France?"
      python3 sim/planner_free.py grok "Summarize the latest crypto trends."
    """

    if len(sys.argv) < 3:
        print("Usage: python3 sim/planner_free.py <target_agent> \"your prompt here\"")
        sys.exit(1)

    target = sys.argv[1]          # e.g. "chatgpt", "grok", "perplexity", "gemini"
    prompt = " ".join(sys.argv[2:])

    task_id = f"task-{uuid.uuid4().hex[:8]}"

    task = {
        "task_id": task_id,
        "target": target,
        "prompt": prompt,
        # You can add params later if you want:
        "params": {
            "max_tokens": 256
        },
        "timestamp": time.time(),
    }

    r.publish("plasma_inbox", json.dumps(task))
    print(f"Task {task_id} published to plasma_inbox → target={target}")
    print(f"Prompt: {prompt}")

if __name__ == "__main__":
    main()
