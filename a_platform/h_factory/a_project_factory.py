import logging
from typing import List
from a_platform.b_contracts.e_execution_context import ExecutionContext
from a_platform.b_contracts import Artifact
from a_platform.g_agents.n_factory.a_agent_factory import AgentFactory
from .b_capability_resolver import CapabilityResolver
from .c_artifact_collector import ArtifactCollector
from .d_generation_context import GenerationContext

logger = logging.getLogger(__name__)

class ProjectFactory:
    def __init__(self, agent_factory: AgentFactory):
        self.agent_factory = agent_factory

    def generate(self, request: ExecutionContext) -> List[Artifact]:
        plan = getattr(request.project_context, "plan", [])
        if not plan:
            logger.error("[ProjectFactory] Plano de execução vazio.")
            return []

        capabilities = request.discovery_data.get("capabilities", []) if request.discovery_data else []
        gen_context = GenerationContext(
            project_context=request.project_context,
            capabilities_requested=capabilities,
            resolved_capabilities=CapabilityResolver.resolve(capabilities)
        )
        
        logger.info(f"[ProjectFactory] Resolved Capabilities: {gen_context.resolved_capabilities}")
        
        for task in plan:
            agent_name = getattr(task, "assigned_agent", None)
            if not agent_name:
                logger.error(f"[ProjectFactory] ProjectTask {task.task_id} não possui agente designado.")
                continue
                
            agent_instance = self.agent_factory.get_agent(agent_name)
            if not agent_instance:
                logger.error(f"[ProjectFactory] Agente {agent_name} não encontrado no registro.")
                continue
                
            logger.info(f"[ProjectFactory] Delegando task {task.task_id} para {agent_name}")
            agent_instance = agent_class() # Dependencies should ideally be injected here via a factory method
            
            try:
                # O Agente Base executa as skills/mcps e devolve artifacts reais
                artifacts = agent_instance.execute_task(task, request)
                gen_context.artifacts.extend(artifacts)
            except Exception as e:
                logger.error(f"[ProjectFactory] Agente {agent_name} falhou na task {task.task_id}: {e}")
                # Falha propaga
                raise RuntimeError(f"Geração falhou na task {task.task_id}") from e

        return ArtifactCollector.collect(plan, gen_context.artifacts)
