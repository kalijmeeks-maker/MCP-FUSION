from __future__ import annotations
from typing import Any, Dict
from core.fusion_state import FusionState


def openai_planner(state: FusionState) -> Dict[str, Any]:
    """Mock planner: later you swap this for real OpenAI calls."""
    return {
        "worker": "openai_planner",
        "model": "gpt-mock",
        "job_id": state.job_id,
        "goal": state.goal,
        "action_plan": [
            "Step 1: Clarify constraints.",
            "Step 2: Enumerate options.",
            "Step 3: Propose high-leverage sequence.",
        ],
        "confidence": 0.82,
        "notes": "Mock output – replace with real OpenAI call later.",
    }
