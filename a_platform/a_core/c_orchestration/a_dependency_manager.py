from typing import List, Dict, Set

class DependencyManager:
    def __init__(self):
        self.dependencies: Dict[str, List[str]] = {}

    def add_dependency(self, item: str, depends_on: str):
        if item not in self.dependencies:
            self.dependencies[item] = []
        self.dependencies[item].append(depends_on)

    def resolve(self) -> List[str]:
        resolved: List[str] = []
        seen: Set[str] = set()

        def visit(node: str):
            if node in seen:
                return
            seen.add(node)
            for dep in self.dependencies.get(node, []):
                visit(dep)
            resolved.append(node)

        for item in self.dependencies:
            visit(item)
            
        return resolved
