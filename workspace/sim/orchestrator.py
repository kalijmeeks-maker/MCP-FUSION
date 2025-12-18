#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# --------------------------------------------------------
#  MCP FUSION – ORCHESTRATOR (Clean Full Version)
# --------------------------------------------------------

import os
import json
import time
import redis
import importlib

# -------------------------------------------------------------------
# Memory Engine
# -------------------------------------------------------------------
from sim.memory_engine import search_memory, save_memory

# -------------------------------------------------------------------
# Redis Connection
# -------------------------------------------------------------------
r = redis.Redis(host="localhost", port=6379, db=0)

# -------------------------------------------------------------------
# Simple Role Router
# -------------------------------------------------------------------
def route_for_role(role: str) -> str:
    """
    Map a role in the plan to the correct agent queue.
    """
    role = role.lower().strip()

    if role in ["chatgpt", "writer", "explain"]:
        return "chatgpt"

    if role in ["grok", "researcher", "analysis"]:
        return "grok"

    if role in ["judge", "critic", "eval"]:
        return "judge"

    return "chatgpt"  # fallback


# -------------------------------------------------------------------
# The Example Plan (temporary — replaced later by Autopilot module)
# -------------------------------------------------------------------
plan = {
    "session_id": "0001",
    "steps": [
        {
            "role": "chatgpt",
            "instruction": "Explain Bitcoin like I'm 5."
        },
        {
            "role": "grok",
            "instruction": "Rewrite ChatGPT's answer to be funnier and shorter."
        },
        {
            "role": "judge",
            "instruction": "Evaluate both answers and pick the winner."
        }
    ]
}


# -------------------------------------------------------------------
# Main Execution Function
# -------------------------------------------------------------------
def run_plan(plan_data):
    print("\n[ORCHESTRATOR] Starting session:", plan_data.get("session_id"))
    print("[ORCHESTRATOR] Memory search for ‘Bitcoin’?")
    print(search_memory("bitcoin"))
    print("--------------------------------------------------")

    session_id = plan_data["session_id"]

    # ----------------------------------------------------------
    # Iterate steps
    # ----------------------------------------------------------
    for idx, step in enumerate(plan_data["steps"]):

        agent = route_for_role(step["role"])
        task_id = f"{session_id}-step{idx}"

        task = {
            "task_id": task_id,
            "target": agent,
            "prompt": step["instruction"],
            "metadata": {"role": step["role"], "step": idx}
        }

        # Publish to inbox
        r.publish("plasma_inbox", json.dumps(task))
        print(f"[ORCHESTRATOR] Sent step {idx} → {agent}")

        # ------------------------------------------------------
        # Wait for result
        # ------------------------------------------------------
        p = r.pubsub()
        p.subscribe("plasma_results")

        while True:
            msg = p.get_message()
            if msg and msg["type"] == "message":
                data = json.loads(msg["data"])
                if data.get("task_id") == task_id:
                    print(f"[ORCHESTRATOR] Step {idx} returned.")

                    # Save memory
                    save_memory("result", str(data), agent)

                    break
            time.sleep(0.2)

    print("\n[ORCHESTRATOR] ALL STEPS COMPLETE.")
    print("[ORCHESTRATOR] Memory engine updated.\n")


# -------------------------------------------------------------------
# Entry Point
# -------------------------------------------------------------------
if __name__ == "__main__":
    run_plan(plan)
