import logging
from typing import List
from a_platform.b_contracts.i_execution_context import ExecutionContext
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
        
        from collections import defaultdict, deque
        
        # Build dependency graph
        graph = defaultdict(list)
        in_degree = defaultdict(int)
        task_map = {t.task_id: t for t in plan}
        
        for task in plan:
            in_degree[task.task_id] = 0
            
        for task in plan:
            for dep in task.dependencies:
                graph[dep].append(task.task_id)
                in_degree[task.task_id] += 1
                
        queue = deque([tid for tid in in_degree if in_degree[tid] == 0])
        sorted_tasks = []
        
        while queue:
            curr_id = queue.popleft()
            sorted_tasks.append(task_map[curr_id])
            for neighbor in graph[curr_id]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    
        if len(sorted_tasks) != len(plan):
            logger.error("[ProjectFactory] O plano possui dependências circulares. Interrompendo geração.")
            raise RuntimeError("Dependências circulares detectadas no plano.")
            
        for task in sorted_tasks:
            agent_name = getattr(task, "assigned_agent", None)
            if not agent_name:
                logger.error(f"[ProjectFactory] ProjectTask {task.task_id} não possui agente designado.")
                raise RuntimeError(f"Task {task.task_id} não possui agente designado.")
                
            agent_instance = self.agent_factory.get_agent(agent_name)
            if not agent_instance:
                logger.error(f"[ProjectFactory] Agente {agent_name} não encontrado no registro para a task {task.task_id}.")
                raise RuntimeError(f"Agente {agent_name} não encontrado no registro para a task {task.task_id}.")
                
            logger.info(f"[ProjectFactory] Delegando task {task.task_id} para {agent_name}")
            
            try:
                # O Agente Base executa as skills/mcps e devolve artifacts reais
                artifacts = agent_instance.execute_task(task, request)
                
                # Validation: expected artifacts produced?
                expected_files = set(task.expected_artifacts)
                produced_files = {a.path for a in artifacts}
                
                missing = expected_files - produced_files
                if missing:
                    logger.error(f"[ProjectFactory] Agente {agent_name} não gerou os artefatos esperados: {missing}")
                    raise RuntimeError(f"Artefatos esperados ausentes: {missing}")
                    
                gen_context.artifacts.extend(artifacts)
            except Exception as e:
                logger.error(f"[ProjectFactory] Agente {agent_name} falhou na task {task.task_id}: {e}")
                # Falha propaga imediatamente (Fail-Fast)
                raise RuntimeError(f"Geração falhou na task {task.task_id}") from e

        return ArtifactCollector.collect(plan, gen_context.artifacts)
