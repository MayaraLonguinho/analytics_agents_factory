from typing import Any, Dict, List, Optional

class KnowledgeRegistry:
    def __init__(self):
        self.knowledge_base: Dict[str, Dict[str, Any]] = {}

    def register(self, knowledge_id: str, content: Dict[str, Any]) -> None:
        self.knowledge_base[knowledge_id] = content

    def get(self, knowledge_id: str) -> Optional[Dict[str, Any]]:
        return self.knowledge_base.get(knowledge_id)

    def search_by_tags(self, tags: List[str]) -> List[Dict[str, Any]]:
        results = []
        for kb in self.knowledge_base.values():
            kb_tags = set(kb.get("tags", []))
            if any(tag in kb_tags for tag in tags):
                results.append(kb)
        return results

    def search_by_domain(self, domain: str) -> List[Dict[str, Any]]:
        return [kb for kb in self.knowledge_base.values() if kb.get("domain") == domain]
