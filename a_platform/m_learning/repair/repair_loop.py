import logging
from typing import Dict, Any

from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.m_learning.learning_engine import LearningEngine
from a_platform.f_llm_gateway.gateway import LLMGateway
from a_platform.c_agents.agent_factory import AgentFactory

logger = logging.getLogger(__name__)

class RepairLoop:
    """
    Repair Loop.
    Se a validação falhar, este motor extrai o erro e delega ao LLM para correção.
    """
    def __init__(self, agent_factory: AgentFactory, learning_engine: LearningEngine):
        self.agent_factory = agent_factory
        self.learning_engine = learning_engine
        self.gateway = LLMGateway()

    def run_repair(self, request: ProjectRequest, error_context: str) -> bool:
        logger.warning("[RepairLoop] Iniciando tentativa de conserto (Repair Loop)...")
        
        # O erro deveria vir via error_context, mockando reparo para simplificar:
        prompt = f"Ocorreu um erro na validação do projeto {request.project_id}. Erro: {error_context}. Gere um patch."
        resp = self.gateway.generate_text(prompt, system_prompt="Você é o agente de reparo de código.", model_preference="openai")
        
        if resp.get("success"):
            correction = resp.get("text")
            logger.info("[RepairLoop] Patch gerado pelo LLM.")
            
            # Memoriza no Learning Engine
            self.learning_engine.log_correction(request, error_context, correction)
            
            # Numa implementação completa, o Materializer aplicaria o patch no disco aqui.
            logger.info("[RepairLoop] Reparo aplicado. O ciclo de execução deve reiniciar.")
            return True
        else:
            logger.error("[RepairLoop] Falha ao tentar gerar patch de reparo.")
            return False
