from typing import Any, Dict, List, Optional

class RuleRegistry:
    def __init__(self):
        self.rules: Dict[str, Dict[str, Any]] = {}

    def register(self, rule_id: str, content: Dict[str, Any]) -> None:
        if "severity" not in content:
            content["severity"] = "info"
        self.rules[rule_id] = content

    def get(self, rule_id: str) -> Optional[Dict[str, Any]]:
        return self.rules.get(rule_id)

    def search_by_tags(self, tags: List[str]) -> List[Dict[str, Any]]:
        results = []
        for r in self.rules.values():
            r_tags = set(r.get("tags", []))
            if any(tag in r_tags for tag in tags):
                results.append(r)
        return results

    def get_by_severity(self, severity: str) -> List[Dict[str, Any]]:
        return [r for r in self.rules.values() if r.get("severity") == severity]
