from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Task:
    id: str
    name: str
    description: str
    agent: str
    skills: List[str] = field(default_factory=list)
    mcps: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    expected_artifacts: List[str] = field(default_factory=list)

@dataclass
class ProjectPlan:
    project_id: str
    domain: str
    tasks: List[Task] = field(default_factory=list)
    materializer: str = "generic_materializer"
    validated: bool = False
    
    def add_task(self, task: Task):
        self.tasks.append(task)
