import os
import yaml
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
        
    def get_learned_rules_for_domain(self, domain: str) -> List[Dict[str, Any]]:
        domain = domain.lower()
        base_dir = os.path.dirname(os.path.dirname(__file__))
        rules_path = os.path.join(base_dir, "a_knowledge", "domains", domain, "learned_rules.yaml")
        
        if os.path.exists(rules_path):
            try:
                with open(rules_path, "r") as f:
                    data = yaml.safe_load(f)
                    if isinstance(data, dict) and "rules" in data:
                        return data["rules"]
                    elif isinstance(data, list):
                        return data
            except Exception:
                pass
        return []
