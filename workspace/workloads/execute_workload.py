from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ExecResult:
    ok: bool
    message: str
    output_dir: str
    created: List[str]
    ran: List[Dict[str, Any]]
    errors: List[str]


def _write_file(root: Path, rel_path: str, content: str) -> str:
    p = root / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return str(p)


def _run_cmd(root: Path, cmd: str) -> Dict[str, Any]:
    proc = subprocess.run(
        ["/bin/bash", "-lc", cmd],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-4000:],
        "stderr": proc.stderr[-4000:],
    }


def execute_workload(spec: Dict[str, Any], *, output_dir: Optional[str] = None) -> ExecResult:
    created: List[str] = []
    ran: List[Dict[str, Any]] = []
    errors: List[str] = []

    wid = spec.get("id", "workload")
    out = output_dir or spec.get("output_dir") or f"/tmp/fusion_out/{wid}"
    root = Path(out).expanduser()
    root.mkdir(parents=True, exist_ok=True)

    for d in spec.get("directories", []) or []:
        try:
            p = root / d["path"]
            p.mkdir(parents=True, exist_ok=True)
            created.append(str(p))
        except Exception as e:
            errors.append(f"mkdir {d}: {type(e).__name__}: {e}")

    for f in spec.get("files", []) or []:
        try:
            created.append(_write_file(root, f["path"], f.get("content", "")))
        except Exception as e:
            errors.append(f"write {f.get(path)}: {type(e).__name__}: {e}")

    for c in spec.get("commands", []) or []:
        cmd = c.get("run") or ""
        if not cmd:
            continue
        res = _run_cmd(root, cmd)
        ran.append({"name": c.get("name"), **res})
        if res["returncode"] != 0:
            errors.append(f"command failed: {c.get(name)}: rc={res[returncode]}")

    ok = len(errors) == 0
    msg = "Workload executed" if ok else "Workload executed with errors"
    return ExecResult(ok=ok, message=msg, output_dir=str(root), created=created, ran=ran, errors=errors)
