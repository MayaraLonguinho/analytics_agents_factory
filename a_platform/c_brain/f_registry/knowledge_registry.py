from typing import Dict, Any, List

class BaseRegistry:
    def __init__(self):
        self._data = {}

    def register(self, key: str, value: Dict[str, Any]):
        self._data[key] = value

    def search_by_domain(self, domain: str) -> List[Dict[str, Any]]:
        return [v for v in self._data.values() if v.get("domain") == domain]

    def search_by_tags(self, tags: List[str]) -> List[Dict[str, Any]]:
        result = []
        for v in self._data.values():
            v_tags = v.get("tags", [])
            if any(t in v_tags for t in tags):
                result.append(v)
        return result

class KnowledgeRegistry(BaseRegistry):
    def get_learned_rules_for_domain(self, domain: str) -> List[Dict[str, Any]]:
        return []

