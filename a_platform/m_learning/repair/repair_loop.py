import logging
import json
import re
import os
from typing import Dict, Any

from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.m_learning.learning_engine import LearningEngine
from a_platform.f_llm_gateway.gateway import LLMGateway
from a_platform.c_agents.agent_factory import AgentFactory
from a_platform.e_mcp.mcp_executor import MCPExecutor

logger = logging.getLogger(__name__)

class RepairLoop:
    """
    Repair Loop.
    Se a execução ou validação falhar, este motor extrai o erro e delega ao LLM para correção.
    """
    def __init__(self, agent_factory: AgentFactory, learning_engine: LearningEngine):
        self.agent_factory = agent_factory
        self.learning_engine = learning_engine
        self.gateway = LLMGateway()
        self.mcp = MCPExecutor()

    def run_repair(self, request: ProjectRequest) -> bool:
        logger.warning("[RepairLoop] Iniciando tentativa de conserto (Repair Loop)...")
        
        # Recupera o erro exato que causou a falha
        exec_err = request.metadata.get("execution_error")
        val_err = request.metadata.get("validation_error")
        
        error_context = exec_err if exec_err else val_err
        if not error_context:
            logger.error("[RepairLoop] Nenhum erro encontrado no metadata para reparo.")
            return False
            
        system_prompt = (
            "Você é o SRE (Site Reliability Engineer) de auto-reparo do sistema.\n"
            "Dado um erro de execução ou teste, identifique qual arquivo precisa de correção.\n"
            "Retorne APENAS um JSON válido no formato:\n"
            "{\n"
            '  "file_name": "nome_do_arquivo.py",\n'
            '  "fixed_content": "CONTEUDO COMPLETO E CORRIGIDO DO ARQUIVO"\n'
            "}"
        )
        
        prompt = (
            f"Projeto ID: {request.project_id}\n"
            f"Erro Detectado:\n{error_context}\n\n"
            "Gere a versão corrigida do arquivo problemático."
        )
        
        resp = self.gateway.generate_text(prompt, system_prompt=system_prompt, model_preference="openai")
        
        if resp.get("success"):
            text = resp.get("text", "")
            match = re.search(r'```(?:json)?(.*?)```', text, re.DOTALL)
            if match:
                text = match.group(1).strip()
                
            try:
                repair_data = json.loads(text)
                file_name = repair_data.get("file_name")
                fixed_content = repair_data.get("fixed_content")
                
                if not file_name or not fixed_content:
                    logger.error("[RepairLoop] O LLM não retornou file_name ou fixed_content válidos.")
                    return False
                    
                # Aplicando o patch
                domain = request.discovery_data.get("domain", "generic").lower()
                file_path = os.path.join(os.getcwd(), "e_generated_projects", domain, request.project_id, file_name)
                
                logger.info(f"[RepairLoop] Aplicando patch corretivo em: {file_name}")
                res = self.mcp.execute_tool("filesystem_mcp", action="write", path=file_path, content=fixed_content)
                
                if res.get("success"):
                    logger.info("[RepairLoop] Patch aplicado com sucesso no disco.")
                    # Memoriza no Learning Engine
                    self.learning_engine.log_correction(request, error_context, f"Fixed {file_name}")
                    
                    # Limpa o erro atual para permitir re-execução limpa
                    if "execution_error" in request.metadata: del request.metadata["execution_error"]
                    if "validation_error" in request.metadata: del request.metadata["validation_error"]
                    
                    return True
                else:
                    logger.error(f"[RepairLoop] Falha ao escrever arquivo corrigido: {res.get('error')}")
                    return False
                    
            except Exception as e:
                logger.error(f"[RepairLoop] Falha ao parsear JSON de reparo: {e}")
                return False
        else:
            logger.error("[RepairLoop] Falha ao invocar LLM para gerar patch de reparo.")
            return False
