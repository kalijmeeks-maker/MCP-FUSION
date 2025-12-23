"""
Executor: scaffold-python-cli
Creates a basic Python CLI project from workload spec
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, Any

WORKLOAD_ID = "scaffold-python-cli"

def can_handle(workload: Dict[str, Any]) -> bool:
    return workload.get("id") == WORKLOAD_ID

def execute(workload: Dict[str, Any]) -> Dict[str, Any]:
    root = Path.cwd() / "generated" / WORKLOAD_ID
    root.mkdir(parents=True, exist_ok=True)

    # Create directories
    for d in workload.get("directories", []):
        (root / d["path"]).mkdir(parents=True, exist_ok=True)

    # Create files
    for f in workload.get("files", []):
        p = root / f["path"]
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f.get("content", ""), encoding="utf-8")

    results = []

    # Run commands
    for cmd in workload.get("commands", []):
        res = subprocess.run(
            cmd["run"],
            shell=True,
            cwd=root,
            capture_output=True,
            text=True,
        )
        results.append({
            "name": cmd["name"],
            "returncode": res.returncode,
            "stdout": res.stdout,
            "stderr": res.stderr,
        })

    return {
        "ok": True,
        "workload_id": WORKLOAD_ID,
        "output_path": str(root),
        "commands": results,
    }
