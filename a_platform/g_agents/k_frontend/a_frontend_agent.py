import logging
from typing import List

from a_platform.g_agents.a_base.a_base_agent import BaseAgent
from a_platform.b_contracts import ProjectTask as ProjectTask
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts import Artifact

logger = logging.getLogger(__name__)

def inject_dependencies(task: ProjectTask, request: ExecutionContext) -> str:
    # Simula injecao de dependencias do contexto
    return ""

class FrontendAgent(BaseAgent):
    def execute_task(self, task: ProjectTask, request: ExecutionContext) -> List[Artifact]:
        logger.info(f"[{self.name}] Executando task FrontendAgent: {task.name}")
        
        # As skills devem vir estritamente da task resolvida pelo Planner
        if not task.required_skills:
            logger.warning(f"[{self.name}] Nenhuma skill foi enviada pelo Planner para a task {task.name}.")
            
        task.description = f"{task.description}\n\n{inject_dependencies(task, request)}"
        
        # O BaseAgent ja cuidara de usar o SkillRegistry para executar as task.required_skills
        artifacts = super().execute_task(task, request)
        
        return artifacts
