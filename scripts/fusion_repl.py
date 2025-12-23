#!/usr/bin/env python3
"""
fusion_repl.py - Interactive REPL for MCP-FUSION

This script provides an interactive command-line interface for submitting
tasks to the MCP-FUSION orchestration system via Redis.

Usage:
    python scripts/fusion_repl.py

Environment Variables:
    FUSION_TASK_LIST: Redis list for tasks (default: fusion_tasks)
    FUSION_RESULT_LIST: Redis list for results (default: plasma_results)
    FUSION_WAIT_S: Wait time for results in seconds (default: 1.0)
"""

import json
import subprocess
import sys
import time
import os


TASK_LIST = os.environ.get("FUSION_TASK_LIST", "fusion_tasks")
RESULT_LIST = os.environ.get("FUSION_RESULT_LIST", "plasma_results")
WAIT_TIME = float(os.environ.get("FUSION_WAIT_S", "1.0"))


def sh(*args):
    """Execute shell command and return stripped output."""
    return subprocess.check_output(list(args), text=True).strip()


def redis_lpush(list_name, value):
    """Push a value to a Redis list."""
    subprocess.run(["redis-cli", "LPUSH", list_name, value], check=True)


def redis_lrange(list_name, start, stop):
    """Get a range from a Redis list."""
    return sh("redis-cli", "LRANGE", list_name, str(start), str(stop))


def main():
    """Main REPL loop."""
    print("=" * 60)
    print("MCP-FUSION Interactive REPL")
    print("=" * 60)
    print(f"Task Queue:   {TASK_LIST}")
    print(f"Result Queue: {RESULT_LIST}")
    print(f"Wait Time:    {WAIT_TIME}s")
    print()
    print("Type your prompts below. Press Ctrl+C to exit.")
    print("=" * 60)
    print()

    while True:
        try:
            # Get user input
            task = input("fusion> ").strip()
            
            if not task:
                continue

            # Build task payload
            payload = {
                "task": task,
                "constraints": {
                    "format": "json",
                    "no_markdown": True
                }
            }

            # Push to Redis task queue
            redis_lpush(TASK_LIST, json.dumps(payload))
            print(f"→ Task submitted to {TASK_LIST}")

            # Wait for coordinator to process
            time.sleep(WAIT_TIME)

            # Fetch latest result
            try:
                latest = redis_lrange(RESULT_LIST, 0, 0)
                if latest and latest != "(empty array)":
                    print(f"← Result from {RESULT_LIST}:")
                    print(latest)
                else:
                    print(f"⚠ No results yet in {RESULT_LIST}")
            except subprocess.CalledProcessError as e:
                print(f"⚠ Could not fetch results: {e}")

            print()

        except KeyboardInterrupt:
            print("\n\nExiting MCP-FUSION REPL. Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}")
            print()


if __name__ == "__main__":
    main()
