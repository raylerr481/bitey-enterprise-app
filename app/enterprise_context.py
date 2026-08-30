"""Core domain model for isolated Bitey enterprise assistants."""
from __future__ import annotations
from dataclasses import asdict, dataclass, field
from typing import Any
import re

@dataclass
class Evidence:
    source_type: str
    source_ref: str
    claim: str
    verified: bool = False

@dataclass
class EnterpriseContext:
    company_id: str
    assistant_id: str
    assistant_name: str
    business_study: dict[str, Any] = field(default_factory=dict)
    known_facts: dict[str, Any] = field(default_factory=dict)
    missing_facts: list[str] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)
    hypotheses: list[dict[str, Any]] = field(default_factory=list)
    sources: list[dict[str, Any]] = field(default_factory=list)

    def add_fact(self, key: str, value: Any, evidence: Evidence) -> None:
        if not evidence.verified:
            raise ValueError("A fact requires verified evidence")
        self.known_facts[key] = value
        self.evidence.append(evidence)

    def add_hypothesis(self, claim: str, confidence: float, reason: str) -> None:
        self.hypotheses.append({"claim": claim, "confidence": confidence, "reason": reason})

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["evidence"] = [asdict(x) for x in self.evidence]
        return data

def make_assistant_name(name: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9À-ÿ _-]", "", name).strip()
    if not cleaned:
        raise ValueError("assistant_name is required")
    return cleaned[:80]

def create_enterprise_context(company_name: str, assistant_name: str, *, company_id: str = "new") -> EnterpriseContext:
    if not company_name.strip():
        raise ValueError("company_name is required")
    clean = make_assistant_name(assistant_name)
    assistant_id = re.sub(r"[^a-z0-9-]", "-", clean.lower()).strip("-") or "assistant"
    return EnterpriseContext(company_id=company_id, assistant_id=assistant_id, assistant_name=clean)
