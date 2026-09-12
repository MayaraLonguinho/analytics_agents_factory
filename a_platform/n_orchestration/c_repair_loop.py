import logging
import json
import re
import os
from typing import Dict, Any

from a_platform.a_core.d_session.b_context import ExecutionContext
from a_platform.j_runtime.a_execution.c_runtime import ExecutionResult
from a_platform.n_learning.e_learning_engine import LearningEngine
from a_platform.g_llm_gateway.e_gateway import LLMGateway
from a_platform.d_agents.m_agent_factory.a_agent_factory import AgentFactory
from a_platform.f_mcp.e_executor.a_executor import MCPExecutor

logger = logging.getLogger(__name__)

class RepairLoop:
    """
    Repair Loop.
    Se a execução falhar, este motor extrai o diagnosis do ExecutionResult e delega ao LLM para correção.
    """
    def __init__(self, agent_factory: AgentFactory, learning_engine: LearningEngine):
        self.agent_factory = agent_factory
        self.learning_engine = learning_engine
        self.gateway = LLMGateway()
        self.mcp = MCPExecutor()

    def run_repair(self, request: ExecutionContext, execution_result: ExecutionResult) -> bool:
        attempts = request.architecture_decision.get("repair_attempts", 0)
        if attempts >= 3:
            logger.error("[RepairLoop] Limite máximo de tentativas de reparo excedido (3). O projeto falhou.")
            return False
            
        request.architecture_decision["repair_attempts"] = attempts + 1
        logger.warning(f"[RepairLoop] Iniciando tentativa de conserto (Repair Loop) - Tentativa {request.architecture_decision['repair_attempts']}/3...")
        
        # Recupera o erro exato que causou a falha baseado no runtime
        error_context = execution_result.diagnosis
        
        if not error_context:
            logger.error("[RepairLoop] Nenhum erro encontrado no ExecutionResult (diagnosis vazio).")
            return False
            
        system_prompt = (
            "Você é o Classificador de Falhas do sistema.\n"
            "Dado um erro de execução ou teste, identifique qual arquivo precisa de correção e qual tipo de agente deve consertá-lo.\n"
            "Retorne APENAS um JSON válido no formato:\n"
            "{\n"
            '  "file_name": "nome_do_arquivo.py",\n'
            '  "agent_type": "backend",\n'
            '  "fixed_content": "CONTEUDO COMPLETO E CORRIGIDO DO ARQUIVO"\n'
            "}"
        )
        
        prompt = (
            f"Projeto ID: {request.project_id}\n"
            f"Erro Detectado (Diagnosis):\n{error_context}\n\n"
            f"Stderr completo (opcional, para contexto): {execution_result.stderr[:2000]}\n\n"
            "Gere a versão corrigida do arquivo problemático e identifique o agente especialista responsável."
        )
        
        import asyncio
        resp = asyncio.run(self.gateway.generate(prompt, system_prompt=system_prompt))
        
        text = ""
        if resp and getattr(resp, "content", None):
            text = resp.content.strip()
            
        match = re.search(r'```(?:json)?(.*?)```', text, re.DOTALL)
        if match:
            text = match.group(1).strip()
            
        try:
            repair_data = json.loads(text)
            file_name = repair_data.get("file_name")
            fixed_content = repair_data.get("fixed_content")
            agent_type = repair_data.get("agent_type", "TestingAgent")
            
            if not file_name or not fixed_content:
                logger.error("[RepairLoop] O LLM não retornou file_name ou fixed_content válidos.")
                return False
                
            specialist_agent = self.agent_factory.get_agent(agent_type)
            logger.info(f"[RepairLoop] Agente especialista acionado para reparo: {specialist_agent.name}")
            
            domain = request.domain or "analytics"
            file_path = os.path.join(os.getcwd(), "e_generated_projects", domain, request.project_id, file_name)
            
            logger.info(f"[RepairLoop] Aplicando patch corretivo em: {file_name}")
            res = self.mcp.execute("filesystem_mcp", operation="write", path=file_path, content=fixed_content)
            
            if res.get("status") == "ok":
                logger.info("[RepairLoop] Patch aplicado com sucesso no disco.")
                logger.info(f"[RepairLoop] Correction logged: Fixed {file_name}")
                return True
            else:
                logger.error(f"[RepairLoop] Falha ao escrever arquivo corrigido: {res.get('message')}")
                return False
                
        except Exception as e:
            logger.error(f"[RepairLoop] Falha ao parsear JSON de reparo: {e}")
            return False
