from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List
import uuid
import time


@dataclass
class FusionState:
    job_id: str
    user_id: str
    agent_role: str
    goal: str
    context: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def new(cls, goal: str, user_id: str = "kali", agent_role: str = "coordinator") -> "FusionState":
        return cls(
            job_id=str(uuid.uuid4()),
            user_id=user_id,
            agent_role=agent_role,
            goal=goal,
            metadata={"created_at": time.time()},
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
