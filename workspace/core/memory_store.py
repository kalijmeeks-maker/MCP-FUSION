from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Dict, Any


MEMORY_DIR = Path(__file__).parent.parent / "memory"
MEMORY_DIR.mkdir(exist_ok=True)


def append_event(event: Dict[str, Any]) -> None:
    """
    Append an immutable execution event to a JSONL log.
    """
    record = {
        "ts": time.time(),
        **event,
    }

    path = MEMORY_DIR / "fusion_events.jsonl"
    with path.open("a") as f:
        f.write(json.dumps(record) + "\n")
