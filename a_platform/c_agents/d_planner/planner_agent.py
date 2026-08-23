import logging
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.project_plan import ProjectPlan, Task
from a_platform.h_domains.domain_registry import DomainRegistry

logger = logging.getLogger(__name__)

class PlannerAgent:
    """
    Transforma as Decisões de Arquitetura em um ProjectPlan executável completo.
    """
    def __init__(self, registry: DomainRegistry):
        self.registry = registry

    def generate_plan(self, request: ProjectRequest) -> bool:
        logger.info("Iniciando Planner Agent...")
        
        domain_name = request.discovery_data.get("domain", "generic")
        domain_config = self.registry.get_domain_config(domain_name)
        
        plan = ProjectPlan(
            project_id=request.project_id,
            domain=domain_name,
            materializer=domain_config.get("materializers", ["generic_materializer"])[0]
        )
        
        task_id = 1
        for agent in domain_config.get("agents", []):
            task = Task(
                id=f"t_{task_id}",
                name=f"Executar {agent}",
                description=f"Tarefa alocada para o {agent} gerar artefatos base.",
                agent=agent,
                skills=domain_config.get("skills", []),
                mcps=domain_config.get("mcps", []),
                dependencies=[f"t_{task_id - 1}"] if task_id > 1 else [],
                expected_artifacts=[f"{agent}_output.py"]
            )
            plan.add_task(task)
            
            # Infer run command based on generated script
            plan.run_commands.append(f"./venv/bin/python {agent}_output.py")
            task_id += 1
            
        if not plan.tasks:
            logger.error("Plano gerado está vazio. Falha na validação do plano.")
            return False
            
        plan.validated = True
        request.project_plan = plan
        
        logger.info(f"Plano estruturado com sucesso. Total de tarefas: {len(plan.tasks)}")
        return True
