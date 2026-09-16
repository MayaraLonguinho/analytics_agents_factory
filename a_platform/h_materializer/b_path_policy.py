import os
from pathlib import Path
from typing import Optional

class PathPolicy:
    @staticmethod
    def resolve_and_verify(base_path: str, relative_path: str) -> Optional[str]:
        base = Path(base_path).resolve()
        target = (base / relative_path).resolve()
        
        # Impede path traversal se target não for filho de base
        try:
            target.relative_to(base)
            return str(target)
        except ValueError:
            return None
