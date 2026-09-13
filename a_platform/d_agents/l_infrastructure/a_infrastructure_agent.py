import logging
from typing import List

from a_platform.d_agents.p_base.a_base_agent import BaseAgent
from a_platform.a_core.a_contracts.d_project_contract import ProjectTask as Task
from a_platform.a_core.d_session.b_context import SessionContext as ExecutionContext
from a_platform.a_core.a_contracts.d_project_contract import Artifact

logger = logging.getLogger(__name__)

def inject_dependencies(task: Task, request: ExecutionContext) -> str:
    # Simula injecao de dependencias do contexto
    return ""

class InfrastructureAgent(BaseAgent):
    def execute_task(self, task: Task, request: ExecutionContext) -> List[Artifact]:
        logger.info(f"[{self.name}] Executando task InfrastructureAgent: {task.name}")
        
        # As skills devem vir estritamente da task resolvida pelo Planner
        if not task.skills:
            logger.warning(f"[{self.name}] Nenhuma skill foi enviada pelo Planner para a task {task.name}.")
            
        task.description = f"{task.description}\n\n{inject_dependencies(task, request)}"
        
        # O BaseAgent ja cuidara de usar o SkillRegistry para executar as task.skills
        artifacts = super().execute_task(task, request)
        
        return artifacts
