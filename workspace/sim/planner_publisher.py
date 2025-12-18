#!/usr/bin/env python3
"""
Free-text planner publisher for MCP-FUSION.

Publishes tasks to: plasma_inbox

Usage (non-interactive):
  python3 sim/planner_publisher.py --target chatgpt --prompt "Explain Bitcoin like I'm 12."

If no CLI args are provided, it will prompt you in the terminal.
"""

import argparse
import json
import uuid
import redis

# Redis connection
r = redis.Redis(host="localhost", port=6379, db=0)


def send_task(target: str, prompt: str, max_tokens: int = 512) -> None:
    task = {
        "task_id": f"task-{uuid.uuid4().hex[:8]}",
        "target": target,
        "prompt": prompt,
        "params": {"max_tokens": max_tokens},
    }

    r.publish("plasma_inbox", json.dumps(task))
    print("\n[PLANNER] Task published to plasma_inbox:")
    print(json.dumps(task, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Free-text planner publisher")
    parser.add_argument("--target", "-t", help="Target agent (chatgpt, grok, etc.)")
    parser.add_argument("--prompt", "-p", help="Prompt text to send")
    parser.add_argument("--max-tokens", "-m", type=int, default=512)

    args = parser.parse_args()

    target = args.target
    prompt = args.prompt

    # Interactive fallback
    if not target:
        target = input("Target agent [chatgpt/grok/other] (default=chatgpt): ").strip() or "chatgpt"

    if not prompt:
        print("Enter your prompt. Finish with an empty line:")
        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        prompt = "\n".join(lines).strip()

    if not prompt:
        print("[PLANNER] No prompt provided. Aborting.")
        return

    send_task(target=target, prompt=prompt, max_tokens=args.max_tokens)


if __name__ == "__main__":
    main()
