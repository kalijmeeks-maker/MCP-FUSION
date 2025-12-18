# [EDIT] /Users/kalimeeks/GEMINI-STACK/workspace/MCP-FUSION/workspace/tools/debug_publisher.py
import redis
import json
import uuid
import time
import os
import sys

# --- Configuration ---
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
INBOX_CHANNEL = "plasma_inbox"
RESULTS_CHANNEL = "plasma_results"
TARGET_AGENT = "chatgpt"

# --- Main Execution ---

def publish_debug_job():
    """Publishes a hardcoded job to a single agent and waits for the result."""
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        r.ping()
    except redis.exceptions.ConnectionError as e:
        print(f"[ERROR] Could not connect to Redis: {e}")
        print("Please ensure Redis is running and accessible.")
        sys.exit(1)

    task_id = f"debug-task-{uuid.uuid4().hex[:8]}"
    
    # This is the actual schema used by the orchestrator
    task = {
        "task_id": task_id,
        "target": TARGET_AGENT,
        "prompt": "Analyze the following statement for sentiment: 'The new Gemini model is astonishingly fast.'",
        "metadata": {"role": "debug_test", "step": 0}
    }
    
    # Subscribe to the results channel before publishing
    pubsub = r.pubsub()
    pubsub.subscribe(RESULTS_CHANNEL)
    print(f"Subscribed to result channel: {RESULTS_CHANNEL}")

    # Publish the job to the main inbox
    r.publish(INBOX_CHANNEL, json.dumps(task))
    print(f"Published task '{task_id}' to inbox for target '{TARGET_AGENT}'")
    print("Waiting for result...")

    # Wait for the specific result
    final_result = None
    try:
        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                if data.get("task_id") == task_id:
                    print(f"\n--- Result Received for Task {task_id} ---")
                    print(json.dumps(data, indent=2))
                    final_result = data
                    break # Exit after receiving our specific result
    except KeyboardInterrupt:
        print("\n[INFO] Canceled by user.")
    finally:
        pubsub.close()

    if final_result:
        print(f"\n✅ Debug job for agent '{TARGET_AGENT}' completed successfully.")
        return 0
    else:
        print(f"\n❌ Did not receive result for task '{task_id}'.")
        return 1

if __name__ == "__main__":
    # Wait a moment for workers to be ready
    print("Debug publisher starting in 3 seconds...")
    time.sleep(3)
    sys.exit(publish_debug_job())