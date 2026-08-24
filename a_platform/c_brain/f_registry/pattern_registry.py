from typing import Any, Dict, List, Optional

class PatternRegistry:
    def __init__(self):
        self.patterns: Dict[str, Dict[str, Any]] = {}

    def register(self, pattern_id: str, content: Dict[str, Any]) -> None:
        self.patterns[pattern_id] = content

    def get(self, pattern_id: str) -> Optional[Dict[str, Any]]:
        return self.patterns.get(pattern_id)

    def search_by_tags(self, tags: List[str]) -> List[Dict[str, Any]]:
        results = []
        for p in self.patterns.values():
            p_tags = set(p.get("tags", []))
            if any(tag in p_tags for tag in tags):
                results.append(p)
        return results

    def search_by_domain(self, domain: str) -> List[Dict[str, Any]]:
        return [p for p in self.patterns.values() if p.get("domain") == domain]
