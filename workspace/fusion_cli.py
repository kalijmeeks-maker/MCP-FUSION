import os
import sys
import json
from pathlib import Path

from core.fusion_state import FusionState
from core.pipeline_loader import load_pipeline

from workers.openai_worker import openai_planner
from workers.grok_worker import grok_critic
from workers.coordinator_worker import coordinator


AGENT_MAP = {
    "openai_planner": openai_planner,
    "grok_critic": grok_critic,
    "coordinator": coordinator,
}


def print_status(mode: str, raw_args):
    status = {
        "mode": mode,
        "cwd": str(Path.cwd()),
        "env_status": {
            "OPENAI_API_KEY_present": bool(os.getenv("OPENAI_API_KEY")),
            "XAI_API_KEY_present": bool(os.getenv("XAI_API_KEY")),
        },
        "args": raw_args,
    }
    print(json.dumps(status, indent=2))


def run_pipeline(task_name: str):
    pipeline = load_pipeline(task_name)

    state = FusionState.new(
        goal=f"Execute pipeline: {task_name}",
        user_id="kali",
        agent_role="coordinator",
    )

    outputs = {}
    last_planner = None
    last_critic = None

    for agent in pipeline["pipeline"]["agents"]:
        agent_type = agent["type"]
        agent_id = agent["id"]

        if agent_type == "coordinator":
            result = AGENT_MAP[agent_type](task_name, last_planner, last_critic)
        else:
            result = AGENT_MAP[agent_type](state)

        outputs[agent_id] = result

        if agent_type == "openai_planner":
            last_planner = result
        elif agent_type == "grok_critic":
            last_critic = result

    payload = {
        "job_id": state.job_id,
        "pipeline": pipeline["pipeline"]["name"],
        "fusion_state": state.to_dict(),
        "outputs": outputs,
    }

    print(json.dumps(payload, indent=2))


def main():
    raw_args = sys.argv[1:]
    mode = raw_args[0] if raw_args else "NO_MODE"

    if mode == "TEST_FUSION_STATUS":
        print("Fusion CLI starting...")
        print_status(mode, raw_args)
    elif mode.startswith("FUSION_TASK:"):
        task_name = mode.split(":", 1)[1]
        print("Fusion CLI starting (pipeline mode)...")
        run_pipeline(task_name)
    else:
        print("Fusion CLI starting (unknown mode)...")
        print_status(mode, raw_args)


if __name__ == "__main__":
    main()
