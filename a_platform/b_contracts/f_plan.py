
from pydantic import BaseModel, Field
from typing import List, Any
from .e_task import ProjectTask

class ProjectPlan(BaseModel):
    project_id: str
    domain: str = ""
    tasks: List[ProjectTask] = Field(default_factory=list)
    run_commands: List[str] = Field(default_factory=list)

    def get_all_skills(self) -> List[str]:
        """Retorna todas as skills requeridas no projeto, preservando ordem e deduplicando."""
        seen = set()
        skills = []
        for task in self.tasks:
            for s in task.required_skills:
                if s not in seen:
                    seen.add(s)
                    skills.append(s)
        return skills

    def get_all_capabilities(self) -> List[str]:
        """Retorna todas as capabilities demandadas no projeto, preservando ordem e deduplicando."""
        seen = set()
        caps = []
        for task in self.tasks:
            for c in task.get_all_capabilities():
                if c not in seen:
                    seen.add(c)
                    caps.append(c)
        return caps
