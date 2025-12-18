from __future__ import annotations
from typing import Any, Dict, List


def aggregate_responses(responses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Combine planner + critic style outputs into one Fusion decision blob."""
    result: Dict[str, Any] = {
        "agents": responses,
        "meta": {
            "num_agents": len(responses),
        },
    }

    confidences = []
    for r in responses:
        c = r.get("confidence")
        if isinstance(c, (int, float)):
            confidences.append(float(c))

    if confidences:
        result["meta"]["avg_confidence"] = sum(confidences) / len(confidences)

    return result
