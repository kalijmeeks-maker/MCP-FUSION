# [EDIT] /Users/kalimeeks/GEMINI-STACK/workspace/MCP-FUSION/workspace/tools/submit_job.py
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
PIPELINE_ROLES = ["chatgpt", "grok", "judge"]

# --- Main Execution ---

def run_job_pipeline(prompt: str):
    """
    Acts as a simple orchestrator for a dynamic, multi-step job.
    """
    if not prompt:
        print("[ERROR] Prompt cannot be empty.")
        return 1

    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        r.ping()
    except redis.exceptions.ConnectionError as e:
        print(f"[ERROR] Could not connect to Redis: {e}")
        print("Please ensure the MCP-FUSION stack is running.")
        return 1

    session_id = f"cli-job-{uuid.uuid4().hex[:8]}"
    
    # Subscribe to the results channel before starting
    pubsub = r.pubsub()
    pubsub.subscribe(RESULTS_CHANNEL)
    print(f"Subscribed to result channel: {RESULTS_CHANNEL}")

    # --- Pipeline Execution ---
    previous_results = []
    current_prompt = prompt
    final_answer = None

    try:
        for i, role in enumerate(PIPELINE_ROLES):
            task_id = f"{session_id}-step{i}"
            
            # For the judge, the prompt is the collection of previous results
            if role == "judge":
                current_prompt = f"Please evaluate the following inputs and pick a winner:\n\n{json.dumps(previous_results, indent=2)}"

            # Construct the task dictionary
            task = {
                "task_id": task_id,
                "target": role,
                "prompt": current_prompt,
                "metadata": {"role": role, "step": i, "session_id": session_id}
            }
            
            # Publish the task
            r.publish(INBOX_CHANNEL, json.dumps(task))
            print(f"\n[PIPELINE] Sent task '{task_id}' to agent '{role}'...")

            # Wait for the specific result for this task
            while True:
                message = pubsub.get_message(ignore_subscribe_messages=True, timeout=30) # 30-second timeout
                if message:
                    data = json.loads(message['data'])
                    if data.get("task_id") == task_id:
                        print(f"[PIPELINE] Result received for task '{task_id}'.")
                        
                        # Check for agent errors
                        if data.get("error"):
                            print(f"[ERROR] Agent '{data.get('agent')}' reported an error: {data['error']}")
                            raise RuntimeError(f"Agent {data.get('agent')} failed.")

                        # Store result for the judge
                        result_payload = data.get("result", "")
                        previous_results.append({
                            "agent": data.get("agent"),
                            "result": result_payload
                        })

                        # The next prompt is the previous result
                        current_prompt = result_payload
                        
                        # If this was the last step, we have our final answer
                        if role == "judge":
                           final_answer = result_payload

                        break # Move to next step
                else:
                    # We got a message for a different task, ignore it
                    continue
            
                if message is None: # Timeout
                    raise RuntimeError(f"Timeout waiting for result of task '{task_id}'.")

    except RuntimeError as e:
        print(f"\n[ERROR] Pipeline failed: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n[INFO] Canceled by user.")
        return 1
    finally:
        pubsub.close()

    if final_answer:
        print("\n--- Final Result (from Judge) ---")
        print(json.dumps(final_answer, indent=2))
        print("\n✅ Job completed successfully.")
        return 0
    else:
        print("\n❌ Pipeline did not complete or final result was empty.")
        return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python submit_job.py \"<your prompt>\"")
        sys.exit(1)
    
    cli_prompt = " ".join(sys.argv[1:])
    sys.exit(run_job_pipeline(cli_prompt))
