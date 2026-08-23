import logging
import json
from typing import List
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.c_agents.agent_factory import AgentFactory
from a_platform.f_llm_gateway.gateway import LLMGateway

logger = logging.getLogger(__name__)

class ProjectFactory:
    """
    Fábrica Dinâmica de Projetos.
    Lê o ProjectPlan, orquestra a chamada aos Agents/Skills e compila os Artifacts.
    Não possui lógica de geração de negócios hardcoded.
    """
    def __init__(self, agent_factory: AgentFactory):
        self.agent_factory = agent_factory
        self.gateway = LLMGateway()

    def assemble_project(self, request: ProjectRequest) -> List[Artifact]:
        plan = request.project_plan
        if not plan or not plan.tasks:
            logger.error("[ProjectFactory] ProjectPlan ausente ou vazio. Não há como montar o projeto.")
            return []

        logger.info(f"[ProjectFactory] Iniciando montagem do projeto {request.project_id} ({plan.domain})")
        compiled_artifacts = []
        
        # O Factory poderia fazer checagem topológica (DAG) aqui e despachar em ordem, 
        # mas por simplicidade de POC iterativa (já que é sequencial local):
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
        logger.info("[ProjectFactory] Gerando requirements.txt dinâmico via LLM...")
        
        system_prompt = (
            "Sua tarefa é gerar um arquivo 'requirements.txt' válido para Python com base na decisão de arquitetura fornecida.\n"
            "Retorne APENAS o conteúdo do arquivo txt e nada mais, sem markdown, sem explicações."
        )
        
        prompt = f"Decisão de Arquitetura: {json.dumps(request.architecture_decision)}"
        
        resp = self.gateway.generate_text(prompt, system_prompt=system_prompt)
        content = "pandas\n" # fallback
        if resp.get("success"):
            content = resp.get("text", "").strip()
            # Limpa blocos de código se o LLM ignorar a instrução
            if content.startswith("```"):
                lines = content.split('\n')
                if len(lines) > 2:
                    content = "\n".join(lines[1:-1])
                    
        return Artifact(name="requirements.txt", content=content, type="config")
