from __future__ import annotations

import yaml
from pathlib import Path
from typing import Dict, Any


PIPELINE_DIR = Path(__file__).parent.parent / "pipelines"


def load_pipeline(pipeline_name: str) -> Dict[str, Any]:
    path = PIPELINE_DIR / f"{pipeline_name}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Pipeline not found: {path}")

    with path.open("r") as f:
        data = yaml.safe_load(f)

    return data
