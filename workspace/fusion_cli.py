import os
import sys
import json
from pathlib import Path

from core.fusion_state import FusionState
from workers.openai_worker import openai_planner
from workers.grok_worker import grok_critic
from workers.aggregator import aggregate_responses


def print_status(mode: str, raw_args):
    openai_ok = bool(os.getenv("OPENAI_API_KEY"))
    xai_ok = bool(os.getenv("XAI_API_KEY"))

    status = {
        "mode": mode,
        "cwd": str(Path.cwd()),
        "env_status": {
            "OPENAI_API_KEY_present": openai_ok,
            "XAI_API_KEY_present": xai_ok,
        },
        "args": raw_args,
    }

    print(json.dumps(status, indent=2))


def run_fusion_task(task_name: str, raw_args):
    goal_text = f"Execute fusion task: {task_name}"
    state = FusionState.new(goal=goal_text, user_id="kali", agent_role="coordinator")

    # Mock multi-agent calls
    planner_out = openai_planner(state)
    critic_out = grok_critic(state)

    # Merge them
    fused = aggregate_responses([planner_out, critic_out])

    payload = {
        "job_id": state.job_id,
        "task": task_name,
        "goal": goal_text,
        "fusion_state": state.to_dict(),
        "fusion_output": fused,
    }

    print(json.dumps(payload, indent=2))


def main() -> None:
    raw_args = sys.argv[1:]
    mode = raw_args[0] if raw_args else "NO_MODE"

    if mode == "TEST_FUSION_STATUS":
        print("Fusion CLI starting...")
        print_status(mode, raw_args)
    elif mode.startswith("FUSION_TASK:"):
        print("Fusion CLI starting (task mode)...")
        run_fusion_task(mode, raw_args[1:])
    else:
        print("Fusion CLI starting (unknown mode)...")
        print_status(mode, raw_args)


if __name__ == "__main__":
    main()
