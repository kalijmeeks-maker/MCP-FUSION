import json
import redis
from workspace.executors.scaffold_python_cli import (
import workspace.executors.scaffold_python_cli_v2  # v2 scaffold executor
from workspace.executors import scaffold_python_cli_v2
    can_handle as can_handle_scaffold,
    execute as execute_scaffold,
)

r = redis.Redis(decode_responses=True)

def handle_task(task, constraints=None):
    constraints = constraints or {}
    try:
        workload = json.loads(task) if isinstance(task, str) else task

        # --- scaffold-python-cli executor ---
        if can_handle_scaffold(workload):
            return execute_scaffold(workload)
        # ------------------------------------

        return {
            "ok": True,
            "message": "Task received (no executor matched)",
            "task": workload,
            "constraints": constraints,
        }

    except Exception as e:
        return {
            "ok": False,
            "error": str(e),
            "task": task,
        }

def main():
    print("Coordinator started.")
    while True:
        _, task = r.blpop("fusion_tasks")
        result = handle_task(task)
        r.rpush("plasma_results", json.dumps(result))

if __name__ == "__main__":
    main()