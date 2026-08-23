import logging
from typing import List
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.c_agents.agent_factory import AgentFactory

logger = logging.getLogger(__name__)

class ProjectFactory:
    """
    Fábrica Dinâmica de Projetos.
    Lê o ProjectPlan, orquestra a chamada aos Agents/Skills e compila os Artifacts.
    Não possui lógica de geração de negócios hardcoded.
    """
    def __init__(self, agent_factory: AgentFactory):
        self.agent_factory = agent_factory

    def assemble_project(self, request: ProjectRequest) -> List[Artifact]:
        plan = request.project_plan
        if not plan or not plan.tasks:
            logger.error("[ProjectFactory] ProjectPlan ausente ou vazio. Não há como montar o projeto.")
            return []

        logger.info(f"[ProjectFactory] Iniciando montagem do projeto {request.project_id} ({plan.domain})")
        compiled_artifacts = []
        
        for task in plan.tasks:
            logger.info(f"[ProjectFactory] Despachando task {task.id} para {task.agent}...")
            agent = self.agent_factory.get_agent(task.agent)
            
            # Agent executa a task e devolve artefatos em memória
            task_artifacts = agent.execute_task(task, request)
            
            if not task_artifacts:
                logger.warning(f"[ProjectFactory] O agente {task.agent} não gerou artefatos para a task {task.id}.")
            else:
                compiled_artifacts.extend(task_artifacts)

        # Adiciona artefatos universais (requirements.txt, etc.) gerados dinamicamente
        reqs = self._generate_requirements(request)
        if reqs:
            compiled_artifacts.append(reqs)
            
        logger.info(f"[ProjectFactory] Montagem finalizada. {len(compiled_artifacts)} artefatos compilados.")
        return compiled_artifacts

    def _generate_requirements(self, request: ProjectRequest) -> Artifact:
        domain = request.discovery_data.get("domain", "generic").lower()
        pkgs = ["pandas", "pydantic", "pyyaml"]
        if domain == "data_engineering":
            pkgs.extend(["dbt-core", "sqlalchemy"])
        elif domain in ["crm", "ecommerce"]:
            pkgs.extend(["fastapi", "uvicorn"])
            
        content = "\n".join(pkgs)
        return Artifact(name="requirements.txt", content=content, type="config")
