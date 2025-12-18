#!/usr/bin/env python3
import json
import os
from typing import Any, Dict

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STATE_DIR = os.path.join(WORKSPACE_ROOT, "shared")
STATE_FILE = os.path.join(STATE_DIR, "state.json")


def _ensure_state_file():
    os.makedirs(STATE_DIR, exist_ok=True)
    if not os.path.exists(STATE_FILE):
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)


def read_state() -> Dict[str, Any]:
    _ensure_state_file()
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def write_state(new_state: Dict[str, Any]) -> None:
    _ensure_state_file()
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(new_state, f, indent=2)


def update_state(path: str, value: Any) -> None:
    """
    Update nested key path like 'llama.last_result' = value
    """
    state = read_state()
    parts = path.split(".")
    ref = state
    for p in parts[:-1]:
        if p not in ref or not isinstance(ref[p], dict):
            ref[p] = {}
        ref = ref[p]
    ref[parts[-1]] = value
    write_state(state)
