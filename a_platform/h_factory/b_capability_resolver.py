from typing import List

class CapabilityResolver:
    @staticmethod
    def resolve(requested: List[str]) -> List[str]:
        # Sempre garantimos core capabilities, o resto é derivado da architecture/discovery
        resolved = ["etl", "database", "analytics", "tests", "documentation"]
        optional = ["dashboard", "chatbot", "backend", "frontend"]
        
        for req in requested:
            if req.lower() in optional and req.lower() not in resolved:
                resolved.append(req.lower())
                
        return resolved
