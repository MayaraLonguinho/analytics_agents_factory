import logging
import json
import re
from enum import Enum, auto
from typing import Any

from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.f_llm_gateway.gateway import LLMGateway

logger = logging.getLogger(__name__)

class DiscoveryStatus(Enum):
    COMPLETE = auto()
    NEEDS_INPUT = auto()
    FAILED = auto()

class DiscoveryAgent:
    def __init__(self):
        self.gateway = LLMGateway()

    def run_discovery(self, request: ProjectRequest) -> DiscoveryStatus:
        logger.info("[DiscoveryAgent] Iniciando Discovery Interativo via LLM...")
        
        history = request.discovery_data.get("history", [])
        
        system_prompt = (
            "Você é o Discovery Agent, um analista de sistemas responsável por mapear requisitos antes de qualquer desenvolvimento.\n"
            "Sua tarefa é analisar o prompt inicial do usuário e o histórico de chat para extrair de forma OBRIGATÓRIA as seguintes informações cruciais sobre o projeto:\n"
            "- domain\n"
            "- objective\n"
            "- users\n"
            "- data_sources\n"
            "- functional_requirements\n"
            "- technical_requirements\n"
            "- database\n"
            "- backend\n"
            "- frontend\n"
            "- infrastructure\n"
            "- testing\n"
            "- documentation\n"
            "- constraints\n\n"
            "Verifique inconsistências entre o prompt e as respostas recentes no histórico. Se o prompt inicial era 'Analytics' e o usuário responder pedindo um carrinho de compras ('Ecommerce'), detecte a inconsistência.\n"
            "Se *qualquer* campo vital estiver faltando OU houver uma inconsistência que precise ser resolvida, retorne uma pergunta clara e objetiva para o usuário no campo 'missing_info_question'.\n"
            "Retorne APENAS um JSON válido no seguinte formato e nada mais:\n"
            "{\n"
            '  "domain": "...",\n'
            '  "objective": "...",\n'
            '  "users": "...",\n'
            '  "data_sources": "...",\n'
            '  "functional_requirements": "...",\n'
            '  "technical_requirements": "...",\n'
            '  "database": "...",\n'
            '  "backend": "...",\n'
            '  "frontend": "...",\n'
            '  "infrastructure": "...",\n'
            '  "testing": "...",\n'
            '  "documentation": "...",\n'
            '  "constraints": "...",\n'
            '  "missing_info_question": "Pergunta se faltar algo ou houver inconsistência, senão null"\n'
            "}"
        )
        
        prompt = f"Prompt Original: {request.prompt}\nHistórico da Conversa: {json.dumps(history, ensure_ascii=False)}"
        
        response = self.gateway.generate_text(prompt, system_prompt=system_prompt, model_preference="openai")
        
        if not response.get("success"):
            logger.error("[DiscoveryAgent] Falha de LLM durante o Discovery.")
            return DiscoveryStatus.FAILED
            
        text = response.get("text", "")
        json_str = text
        match = re.search(r'```(?:json)?(.*?)```', text, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
            
        try:
            data = json.loads(json_str)
        except Exception as e:
            logger.error(f"[DiscoveryAgent] Falha ao parsear JSON do LLM: {e}\nRetorno: {text}")
            return DiscoveryStatus.FAILED
            
        for key in ["domain", "objective", "users", "data_sources", "functional_requirements", 
                   "technical_requirements", "database", "backend", "frontend", "infrastructure", 
                   "testing", "documentation", "constraints"]:
            request.discovery_data[key] = data.get(key)
        
        if data.get("missing_info_question"):
            request.discovery_data["missing_info_question"] = data.get("missing_info_question")
            logger.info(f"[DiscoveryAgent] Faltam informações ou há inconsistência: {data.get('missing_info_question')}")
            return DiscoveryStatus.NEEDS_INPUT
            
        if "missing_info_question" in request.discovery_data:
            del request.discovery_data["missing_info_question"]
            
        request.discovery_data["status"] = "COMPLETE"
        logger.info("[DiscoveryAgent] Discovery concluído com sucesso.")
        return DiscoveryStatus.COMPLETE
