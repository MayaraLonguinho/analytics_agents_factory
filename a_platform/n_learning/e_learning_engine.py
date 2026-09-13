"""Learning engine for the Analytics AI Factory.

Execution -> Feedback -> Knowledge Candidate -> Approval/Policy -> Brain Update.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from .a_brain_updater import BrainUpdater
from .c_feedback_collector import FeedbackCollector
from .d_knowledge_generator import KnowledgeGenerator


@dataclass
class LearningRun:
    job_id: str
    raw_feedback: List[Dict[str, Any]] = field(default_factory=list)
    candidate_knowledge: List[Dict[str, Any]] = field(default_factory=list)
    approved_knowledge: List[Dict[str, Any]] = field(default_factory=list)
    incorporated_knowledge: List[Dict[str, Any]] = field(default_factory=list)
    status: str = "pending"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "job_id": self.job_id,
            "raw_feedback": self.raw_feedback,
            "candidate_knowledge": self.candidate_knowledge,
            "approved_knowledge": self.approved_knowledge,
            "incorporated_knowledge": self.incorporated_knowledge,
            "status": self.status,
        }


class LearningEngine:
    """Coordinates the full learning lifecycle without bypassing the approval gate."""

    def __init__(self, project_root: Optional[Path | str] = None):
        self.project_root = Path(project_root or Path.cwd()).resolve()
        self.feedback_collector = FeedbackCollector(self.project_root)
        self.knowledge_generator = KnowledgeGenerator(self.project_root)
        self.brain_updater = BrainUpdater(self.project_root)

    def execute(self, *, source: str, kind: str, payload: Dict[str, Any], title: str, summary: str, evidence: List[str], confidence: float = 0.0, metadata: Optional[Dict[str, Any]] = None) -> LearningRun:
        raw = self.feedback_collector.collect(
            source=source, kind=kind, payload=payload)
        candidate = self.knowledge_generator.from_feedback(
            title=title, summary=summary, evidence=evidence, confidence=confidence, metadata=metadata)
        decision = self.brain_updater.approve(candidate=candidate.model_dump())
        run = LearningRun(
            job_id=f"learning-{source}-{candidate.ts.replace(':', '-').replace('.', '-')}")
        run.raw_feedback.append(raw.model_dump())
        run.candidate_knowledge.append(candidate.model_dump())

        if decision.approved:
            run.approved_knowledge.append(
                {**candidate.model_dump(), "approval": decision.model_dump()})
            incorporated = self.brain_updater.incorporate(
                approved_payload={**candidate.model_dump(), "approval": decision.model_dump()})
            run.incorporated_knowledge.append(incorporated)
            run.status = "approved_and_incorporated"
        else:
            run.status = "rejected_pending_review"

        return run
