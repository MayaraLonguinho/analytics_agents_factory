"""Collect raw runtime and human feedback before knowledge approval."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
from datetime import datetime, timezone


@dataclass
class FeedbackRecord:
    source: str
    kind: str
    payload: Dict[str, Any]
    ts: str = field(default_factory=lambda: datetime.now(
        timezone.utc).isoformat())
    approved: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "kind": self.kind,
            "payload": self.payload,
            "ts": self.ts,
            "approved": self.approved,
        }


class FeedbackCollector:
    """Persist raw feedback and classify it before approval."""

    def __init__(self, project_root: Optional[Path | str] = None):
        self.project_root = Path(project_root or Path.cwd()).resolve()
        self.feedback_root = self.project_root / "m_learning" / "feedback"
        self.raw_root = self.feedback_root / "raw"
        self.raw_root.mkdir(parents=True, exist_ok=True)

    def collect(self, *, source: str, kind: str, payload: Dict[str, Any]) -> FeedbackRecord:
        record = FeedbackRecord(source=source, kind=kind, payload=payload)
        file_path = self.raw_root / \
            f"{record.ts.replace(':', '-').replace('.', '-')}__{kind}.json"
        file_path.write_text(json.dumps(
            record.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        return record

    def list_raw(self) -> List[Path]:
        return sorted(self.raw_root.glob("*.json"))
