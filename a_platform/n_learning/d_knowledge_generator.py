"""Generate approved knowledge candidates from collected feedback."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
from datetime import datetime, timezone


@dataclass
class KnowledgeCandidate:
    title: str
    summary: str
    evidence: List[str] = field(default_factory=list)
    confidence: float = 0.0
    status: str = "candidate"
    metadata: Dict[str, Any] = field(default_factory=dict)
    ts: str = field(default_factory=lambda: datetime.now(
        timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "summary": self.summary,
            "evidence": self.evidence,
            "confidence": self.confidence,
            "status": self.status,
            "metadata": self.metadata,
            "ts": self.ts,
        }


class KnowledgeGenerator:
    """Transforms raw feedback into a candidate knowledge artifact."""

    def __init__(self, project_root: Optional[Path | str] = None):
        self.project_root = Path(project_root or Path.cwd()).resolve()
        self.feedback_root = self.project_root / "m_learning" / "feedback"
        self.candidate_root = self.feedback_root / "candidate"
        self.candidate_root.mkdir(parents=True, exist_ok=True)

    def from_feedback(self, *, title: str, summary: str, evidence: List[str], confidence: float = 0.0, metadata: Optional[Dict[str, Any]] = None) -> KnowledgeCandidate:
        candidate = KnowledgeCandidate(
            title=title,
            summary=summary,
            evidence=evidence,
            confidence=max(0.0, min(1.0, confidence)),
            metadata=metadata or {},
        )
        file_path = self.candidate_root / \
            f"{candidate.ts.replace(':', '-').replace('.', '-')}__{title.lower().replace(' ', '_')}.json"
        file_path.write_text(json.dumps(
            candidate.model_dump(), indent=2, ensure_ascii=False), encoding="utf-8")
        return candidate

    def list_candidates(self) -> List[Path]:
        return sorted(self.candidate_root.glob("*.json"))
