from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Artifact:
    name: str
    content: str
    type: str = "source_code"  # source_code, script, config, sql, etc.
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
