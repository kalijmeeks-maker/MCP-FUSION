"""
Judge Worker - Rule-based evaluator for comparing provider outputs.

Usage:
    .venv/bin/python -m workspace.workers.judge_worker <path_to_a.json> <path_to_b.json>

Each file should contain a single JSON dict following provider output contract:
    {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "output_text": "...",
        "usage": {"prompt_tokens": N, "completion_tokens": N, "total_tokens": N},
        "error": null
    }
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class JudgeVerdict:
    winner: str
    score_a: float
    score_b: float
    rationale: str
    error: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": "judge",
            "model": os.getenv("JUDGE_MODEL", "rule-based-v0"),
            "output_text": json.dumps(
                {
                    "winner": self.winner,
                    "score_a": self.score_a,
                    "score_b": self.score_b,
                    "rationale": self.rationale,
                },
                ensure_ascii=False,
            ),
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            "error": self.error,
        }


def score_text(text: str) -> float:
    """
    Minimal deterministic scoring:
    - rewards longer, structured, less error-y outputs
    - penalizes obvious failure markers
    Replace later with an LLM-judge call.
    """
    t = (text or "").strip()
    if not t:
        return 0.0
    bad = sum(1 for k in ["error", "exception", "traceback", "mock"] if k in t.lower())
    base = min(len(t) / 800.0, 1.0)  # length reward up to 1.0
    return max(0.0, base - 0.25 * bad)


def judge(a: Dict[str, Any], b: Dict[str, Any]) -> JudgeVerdict:
    ta = a.get("output_text", "") or a.get("completion", "")
    tb = b.get("output_text", "") or b.get("completion", "")
    sa = score_text(ta)
    sb = score_text(tb)
    if sa > sb:
        winner = a.get("provider", "A")
    elif sb > sa:
        winner = b.get("provider", "B")
    else:
        winner = "tie"
    rationale = f"Deterministic rule score: A={sa:.3f}, B={sb:.3f}. Tie-breaker favors higher structure/less failure markers."
    return JudgeVerdict(winner=winner, score_a=sa, score_b=sb, rationale=rationale)


def main() -> None:
    if len(sys.argv) != 3:
        out = JudgeVerdict(
            winner="error",
            score_a=0.0,
            score_b=0.0,
            rationale="invalid args",
            error={"type": "invalid_args", "message": "Expected 2 JSON file paths."},
        )
        print(json.dumps(out.to_dict(), ensure_ascii=False))
        raise SystemExit(2)

    pa, pb = sys.argv[1], sys.argv[2]
    with open(pa, "r", encoding="utf-8") as f:
        a = json.load(f)
    with open(pb, "r", encoding="utf-8") as f:
        b = json.load(f)

    verdict = judge(a, b)
    print(json.dumps(verdict.to_dict(), ensure_ascii=False))


if __name__ == "__main__":
    main()
