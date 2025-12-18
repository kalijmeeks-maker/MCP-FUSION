#!/usr/bin/env python3
"""
Agent planner for MCP-FUSION.

Reads a free-text instruction from you,
chooses an LLM target (chatgpt or grok) using simple rules,
and publishes a task to plasma_inbox.
"""

import json
import uuid
import redis

r = redis.Redis(host="localhost", port=6379, db=0)


def choose_target(prompt: str) -> str:
    """
    Very simple routing logic for now.

    - If prompt mentions "internet", "live data", "news" -> grok
    - If prompt mentions "code", "python", "explain", "step-by-step" -> chatgpt
    - Otherwise default to chatgpt
    """
    p = prompt.lower()

    if any(w in p for w in ["news", "headline", "twitter", "x.com", "live data", "internet"]):
        return "grok"

    if any(w in p for w in ["code", "python", "function", "bug", "stack trace", "step-by-step", "explain"]):
        return "chatgpt"

    # Default
    return "chatgpt"


def send_task(target: str, prompt: str, max_tokens: int = 512) -> None:
    task = {
        "task_id": f"task-{uuid.uuid4().hex[:8]}",
        "target": target,
        "prompt": prompt,
        "params": {"max_tokens": max_tokens},
    }

    r.publish("plasma_inbox", json.dumps(task))
    print("\n[AGENT-PLANNER] Chosen target:", target)
    print("[AGENT-PLANNER] Task published to plasma_inbox:")
    print(json.dumps(task, indent=2))


def main() -> None:
    print("=== MCP-FUSION Agent Planner ===")
    print("Type your instruction. End with an empty line.\n")

    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "":
            break
        lines.append(line)

    prompt = "\n".join(lines).strip()

    if not prompt:
        print("[AGENT-PLANNER] No prompt provided. Aborting.")
        return

    target = choose_target(prompt)
    send_task(target, prompt)


if __name__ == "__main__":
    main()
