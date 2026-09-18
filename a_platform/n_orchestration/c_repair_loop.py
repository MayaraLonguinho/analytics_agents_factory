import logging
from a_platform.b_contracts.e_execution_context import ExecutionContext
from a_platform.b_contracts import ExecutionResult

logger = logging.getLogger(__name__)

class RepairLoop:
    def __init__(self, agent_factory, learning_engine):
        self.agent_factory = agent_factory
        self.learning_engine = learning_engine

    def run_repair(self, request: ExecutionContext, runtime_result: ExecutionResult) -> bool:
        if not runtime_result or runtime_result.status == "PASSED":
            logger.info("Nenhuma falha para reparar.")
            return True
            
        logger.warning(f"Iniciando Repair Loop para a falha. Task: {runtime_result.task_id}, Error: {runtime_result.error}")
        
        # Identify the failed task
        plan = getattr(request.project_context, "plan", [])
        failed_task = None
        for t in plan:
            if t.task_id == runtime_result.task_id:
                failed_task = t
                break
                
        if not failed_task:
            logger.error(f"Task falha não encontrada no plano: {runtime_result.task_id}")
            return False
            
        agent_name = getattr(failed_task, "assigned_agent", None)
        if not agent_name:
            logger.error("A tarefa falha não possui agente designado.")
            return False
            
        agent = self.agent_factory.get_agent(agent_name)
        if not agent:
            logger.error(f"Agente designado {agent_name} não encontrado na Factory.")
            return False
            
        logger.info(f"Invocando agente responsável {agent_name} para realizar o reparo.")
        
        # Criamos um contexto temporário para indicar ao agente a falha no prompt
        original_prompt = request.prompt
        request.prompt = f"REPARO DE TAREFA NECESSÁRIO! A tarefa {failed_task.task_id} falhou.\nComando executado: {runtime_result.command}\nOutput: {runtime_result.stdout}\nErro: {runtime_result.stderr}\nCorrija o código de acordo."
        
        try:
            # Reexecuta a tarefa via agente
            fixed_artifacts = agent.execute_task(failed_task, request)
            
            # Restaura prompt original
            request.prompt = original_prompt
            
            # Rematerializa os artefatos corrigidos
            from a_platform.h_materializer.a_materializer import ArtifactMaterializer
            from a_platform.f_mcps.d_registry.b_executor import MCPExecutor
            mcp = MCPExecutor()
            materializer = ArtifactMaterializer(mcp)
            
            mat_res = materializer.materialize(request, fixed_artifacts)
            if mat_res.status == "FAILED":
                logger.error(f"Materialização do reparo falhou: {mat_res.evidence}")
                return False
                
            logger.info("Reparo concluído e materializado. Solicitando reexecução.")
            return True
        except Exception as e:
            logger.error(f"O agente falhou ao processar o reparo: {e}")
            request.prompt = original_prompt
            return False
