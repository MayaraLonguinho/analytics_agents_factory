"""Approval gate and brain integration for learning artifacts."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import json


@dataclass
class ApprovalDecision:
    approved: bool
    reason: str
    policy: str = "default"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "approved": self.approved,
            "reason": self.reason,
            "policy": self.policy,
            "metadata": self.metadata,
        }


class BrainUpdater:
    """Only updates the official brain after approval and policy checks."""

    def __init__(self, project_root: Optional[Path | str] = None):
        self.project_root = Path(project_root or Path.cwd()).resolve()
        self.feedback_root = self.project_root / "m_learning" / "feedback"
        self.approved_root = self.feedback_root / "approved"
        self.incorporated_root = self.feedback_root / "incorporated"
        self.approved_root.mkdir(parents=True, exist_ok=True)
        self.incorporated_root.mkdir(parents=True, exist_ok=True)
        self.brain_root = self.project_root / "c_brain"
        self.brain_root.mkdir(parents=True, exist_ok=True)

    def approve(self, *, candidate: Dict[str, Any], policy: str = "default") -> ApprovalDecision:
        uses_evidence = bool(candidate.get("evidence"))
        confidence = float(candidate.get("confidence", 0.0))
        approved = uses_evidence and confidence >= 0.7
        reason = "approved by policy" if approved else "rejected: insufficient confidence or evidence"
        decision = ApprovalDecision(
            approved=approved, reason=reason, policy=policy, metadata={"confidence": confidence})
        if approved:
            path = self.approved_root / \
                f"{candidate.get('ts', 'unknown').replace(':', '-').replace('.', '-')}_{candidate.get('title', 'knowledge').lower().replace(' ', '_')}.json"
            path.write_text(json.dumps(candidate, indent=2,
                            ensure_ascii=False), encoding="utf-8")
        return decision

    def incorporate(self, *, approved_payload: Dict[str, Any]) -> Dict[str, Any]:
        # The official brain remains canonical; this updater writes an incorporated learning record behind the approval gate.
        target = self.incorporated_root / \
            f"{approved_payload.get('ts', 'unknown').replace(':', '-').replace('.', '-')}_{approved_payload.get('title', 'knowledge').lower().replace(' ', '_')}.json"
        target.write_text(json.dumps(approved_payload, indent=2,
                          ensure_ascii=False), encoding="utf-8")
        brain_snapshot = self.brain_root / "memory" / "learning"
        brain_snapshot.mkdir(parents=True, exist_ok=True)
        brain_summary = brain_snapshot / "incorporated_knowledge.json"
        existing: List[Dict[str, Any]] = []
        if brain_summary.exists():
            try:
                existing = json.loads(
                    brain_summary.read_text(encoding="utf-8"))
            except Exception:
                existing = []
        existing.append(approved_payload)
        brain_summary.write_text(json.dumps(
            existing, indent=2, ensure_ascii=False), encoding="utf-8")
        return approved_payload
