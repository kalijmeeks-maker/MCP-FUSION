from __future__ import annotations

from typing import Any, Dict
from workspace.workloads.execute_workload import execute_workload


def run(spec: Dict[str, Any]) -> Dict[str, Any]:
    r = execute_workload(spec)
    return {
        "ok": r.ok,
        "message": r.message,
        "workload_id": spec.get("id"),
        "output_dir": r.output_dir,
        "created_count": len(r.created),
        "ran_count": len(r.ran),
        "errors": r.errors,
        "ran": r.ran,
    }
