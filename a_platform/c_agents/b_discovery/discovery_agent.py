import logging
import json
import re
from typing import Any

from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.f_llm_gateway.gateway import LLMGateway

logger = logging.getLogger(__name__)

class DiscoveryAgent:
    def __init__(self):
        self.gateway = LLMGateway()

    def run_discovery(self, request: ProjectRequest) -> bool:
        logger.info("[DiscoveryAgent] Iniciando Discovery Interativo via LLM...")
        
        history = request.discovery_data.get("history", [])
        
        system_prompt = (
            "Você é o Discovery Agent. Sua tarefa é analisar o prompt inicial do usuário e o histórico de chat para extrair as seguintes informações cruciais sobre o projeto:\n"
            "- domain: (ex: Ecommerce, Finanças, Saude, Analytics, etc)\n"
            "- database: (ex: PostgreSQL, MongoDB, SQLite)\n"
            "- restrictions: (ex: Apenas Python 3.10, Sem Docker)\n"
            "- objective: (Breve resumo do que o projeto faz)\n\n"
            "Verifique inconsistências entre o prompt e as respostas recentes no histórico.\n"
            "Se qualquer campo vital estiver faltando OU houver inconsistência (ex: prompt era 'Analytics' mas a conversa mudou para 'Ecommerce'), retorne uma pergunta clara e objetiva para o usuário no campo 'missing_info_question'.\n"
            "Retorne APENAS um JSON válido no seguinte formato e nada mais:\n"
            "{\n"
            '  "domain": "...",\n'
            '  "database": "...",\n'
            '  "restrictions": "...",\n'
            '  "objective": "...",\n'
            '  "missing_info_question": "Pergunta se algo faltar, senao null"\n'
            "}"
        )
        
        prompt = f"Prompt Original: {request.prompt}\nHistórico da Conversa: {json.dumps(history, ensure_ascii=False)}"
        
        response = self.gateway.generate_text(prompt, system_prompt=system_prompt, model_preference="openai")
        
        if not response.get("success"):
            logger.error("[DiscoveryAgent] Falha de LLM durante o Discovery.")
            return False
            
        text = response.get("text", "")
        # Extrair JSON do retorno (tratando possíveis blocos de código)
        json_str = text
        match = re.search(r'```(?:json)?(.*?)```', text, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
            
        try:
            data = json.loads(json_str)
        except Exception as e:
            logger.error(f"[DiscoveryAgent] Falha ao parsear JSON do LLM: {e}\nRetorno: {text}")
            return False
            
        # Merge no request
        request.discovery_data["domain"] = data.get("domain")
        request.discovery_data["database"] = data.get("database")
        request.discovery_data["restrictions"] = data.get("restrictions")
        request.discovery_data["objective"] = data.get("objective")
        
        if data.get("missing_info_question"):
            request.discovery_data["missing_info_question"] = data.get("missing_info_question")
            logger.info(f"[DiscoveryAgent] Faltam informações: {data.get('missing_info_question')}")
            return False # False aqui significa "não completou, pause" pois "missing_info_question" será lido pelo Orchestrator
            
        # Se não há pergunta, o Discovery está completo
        if "missing_info_question" in request.discovery_data:
            del request.discovery_data["missing_info_question"]
            
        request.discovery_data["status"] = "COMPLETE"
        logger.info("[DiscoveryAgent] Discovery concluído com sucesso.")
        return True
