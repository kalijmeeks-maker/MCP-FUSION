import asyncio
import json
from typing import Dict, Any, List

# Assuming a Redis connection similar to other workers
import redis

from workspace.core.llm_clients import get_completions

# --- Configuration ---
# These would typically be loaded from a config file or env vars
REDIS_HOST = "localhost"
REDIS_PORT = 6379
RESULTS_CHANNEL = "plasma_results"


def get_redis_client() -> redis.Redis:
    """Initializes and returns a Redis client."""
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


async def run_and_publish_results(prompt: str, task_id: str, session_id: str):
    """
    Orchestrates fetching completions from multiple LLMs and publishes the result.
    """
    r = get_redis_client()
    
    print(f"[{task_id}] Coordinator received prompt: '{prompt}'")
    
    # 1. Get aggregated results from LLM clients
    aggregated_results = await get_completions(prompt)
    
    # 2. Construct the result payload
    result_payload = {
        "task_id": task_id,
        "session_id": session_id,
        "agent": "coordinator",
        "status": "completed",
        "result": aggregated_results,
    }
    
    # 3. Publish the final result
    r.publish(RESULTS_CHANNEL, json.dumps(result_payload))
    print(f"[{task_id}] Coordinator published final results to {RESULTS_CHANNEL}.")


# Example of how a worker might consume a task and run this.
# This part is for illustration and might live in the worker's main loop.
async def main_worker_loop():
    # This is a simplified representation. A real worker would listen
    # on a Redis channel for incoming tasks.
    
    # Example task received from orchestrator
    example_task = {
        "task_id": "coord-task-123",
        "session_id": "session-456",
        "prompt": "What is the future of multi-agent systems?",
    }
    
    await run_and_publish_results(
        prompt=example_task["prompt"],
        task_id=example_task["task_id"],
        session_id=example_task["session_id"]
    )

if __name__ == "__main__":
    import os
    import sys
    print("Starting coordinator worker (example run)...")
    # To test this file directly, you'd need a running Redis instance
    # and to ensure the OPENAI_API_KEY is set.
    # e.g., `export OPENAI_API_KEY=...`
    
    # Check for Redis connection
    try:
        r = get_redis_client()
        r.ping()
        print("Redis connection successful.")
    except redis.exceptions.ConnectionError as e:
        print(f"Could not connect to Redis: {e}", file=sys.stderr)
        print("Please ensure Redis is running to execute this example.", file=sys.stderr)
        sys.exit(1)

    # Check for API key for testing
    if not os.environ.get("OPENAI_API_KEY"):
        print("\nERROR: OPENAI_API_KEY environment variable not set for testing.", file=sys.stderr)
        sys.exit(1)

    asyncio.run(main_worker_loop())
    print("Coordinator worker example run finished.")
