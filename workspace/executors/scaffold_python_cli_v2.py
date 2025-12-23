from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List


def _slug(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9_-]+", "_", s)
    return s.strip("_") or "project"


def _pkg_name(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_]+", "_", s)
    if not re.match(r"^[a-zA-Z_]", s):
        s = "_" + s
    return s


def can_handle(workload: Dict[str, Any]) -> bool:
    return (workload.get("workload_id") or workload.get("id")) == "scaffold-python-cli-v2"


def _run(cmd: str, cwd: Path) -> Dict[str, Any]:
    p = subprocess.run(
        ["bash", "-lc", cmd],
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )
    return {
        "name": cmd.split()[0],
        "returncode": p.returncode,
        "stdout": p.stdout or "",
        "stderr": p.stderr or "",
    }


def execute(workload: Dict[str, Any]) -> Dict[str, Any]:
    opts = workload.get("options", {})

    project = _slug(opts.get("project_name", "python_cli"))
    package = _pkg_name(opts.get("package_name", project))

    base = Path("/Users/kalimeeks/MCP-FUSION/generated")
    out = base / project
    out.mkdir(parents=True, exist_ok=True)

    src = out / "src" / package
    src.mkdir(parents=True, exist_ok=True)

    (src / "__init__.py").write_text("", encoding="utf-8")

    (src / "__main__.py").write_text(
        "def main():\n"
        "    print(\"hello\")\n\n"
        "if __name__ == \"__main__\":\n"
        "    main()\n",
        encoding="utf-8",
    )

    (out / "pyproject.toml").write_text(
        f"""[project]
name = "{project}"
version = "0.1.0"
requires-python = ">=3.12"

[project.scripts]
{project} = "{package}.__main__:main"
""",
        encoding="utf-8",
    )

    cmds: List[Dict[str, Any]] = []
    cmds.append(_run("python -m venv .venv", out))
    cmds.append(_run("source .venv/bin/activate && python -m pip install -U pip", out))
    cmds.append(_run(f"source .venv/bin/activate && python -m {package}", out))

    return {
        "ok": True,
        "workload_id": "scaffold-python-cli-v2",
        "output_path": str(out),
        "commands": cmds,
    }
