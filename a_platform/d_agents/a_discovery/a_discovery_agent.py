import logging
import json
import re
from enum import Enum, auto
from typing import Any

from a_platform.a_core.d_session.b_context import ExecutionContext, Decision
from a_platform.g_llm_gateway.e_gateway import LLMGateway

logger = logging.getLogger(__name__)

class DiscoveryStatus(Enum):
    COMPLETE = auto()
    NEEDS_INPUT = auto()
    FAILED = auto()

class DiscoveryAgent:
    def __init__(self, gateway: LLMGateway, max_questions=5):
        self.gateway = gateway
        self.max_questions = max_questions

    async def run_discovery(self, context: ExecutionContext, brain_instance: Any = None) -> DiscoveryStatus:
        logger.info("[DiscoveryAgent] Iniciando Discovery Interativo via LLM...")
        
        # Ensure discovery_data structure exists in memory temporarily for tracking
        if not hasattr(context, "_discovery_data"):
            context._discovery_data = {"history": [], "question_count": 0}
            
        history = context._discovery_data.get("history", [])
        q_count = context._discovery_data.get("question_count", 0)
        
        # Check limit
        if q_count >= self.max_questions:
            logger.info("[DiscoveryAgent] Limite de perguntas atingido. Congelando com defaults do Brain.")
            if brain_instance:
                # Mock a request for brain intelligent defaults
                req = {"domain": context.domain or "data_engineering", "architecture": context.architecture_decision}
                req = brain_instance.apply_intelligent_defaults(req)
                context.architecture_decision = req.get("architecture", {})
            
            context.add_decision(Decision(
                id=f"D-DISC-00{len(context.decisions)+1}",
                status="adopted",
                decision="Assumed intelligent defaults due to max questions limit.",
                reason="Max discovery questions reached."
            ))
            context.freeze_context()
            return DiscoveryStatus.COMPLETE

        system_prompt = (
            "Você é o Discovery Agent. Sua tarefa é mapear os requisitos. "
            "Você pode fazer APENAS UMA pergunta por vez ao usuário, e NO MÁXIMO 5 ao longo de toda a sessão. "
            "Faça perguntas SOMENTE se mudarem drasticamente a arquitetura, escopo, capability ou critério de aceite. "
            "Para dúvidas menores, assuma um default razoável. "
            "Se o usuário respondeu algo crítico, extraia as variáveis e as anote. "
            "Extraia obrigatoriamente: project_type, business_context, domain. "
            "Retorne APENAS um JSON válido no formato:\n"
            "{\n"
            '  "project_type": "...",\n'
            '  "business_context": "...",\n'
            '  "domain": "...",\n'
            '  "assumed_defaults": [{"decision": "...", "reason": "..."}],\n'
            '  "user_decisions": [{"decision": "...", "reason": "..."}],\n'
            '  "missing_info_question": "Pergunta se for crítico, senão null"\n'
            "}"
        )
        
        prompt = f"Prompt Original: {context.prompt}\nHistórico da Conversa: {json.dumps(history, ensure_ascii=False)}\nPerguntas feitas: {q_count}/{self.max_questions}"
        
        response = await self.gateway.generate(prompt, system_prompt=system_prompt)
        
        if not response or not response.content:
            logger.error("[DiscoveryAgent] Falha de LLM durante o Discovery.")
            return DiscoveryStatus.FAILED
            
        text = response.content or ""
        json_str = text
        match = re.search(r'```(?:json)?(.*?)```', text, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
            
        try:
            data = json.loads(json_str)
        except Exception as e:
            logger.error(f"[DiscoveryAgent] Falha ao parsear JSON do LLM: {e}\nRetorno: {text}")
            return DiscoveryStatus.FAILED
            
        if data.get("project_type"):
            context.project_type = data.get("project_type")
        if data.get("business_context"):
            context.business_context = data.get("business_context")
        if data.get("domain"):
            context.domain = data.get("domain")
        
        # Registrar D-NN
        for d in data.get("assumed_defaults", []):
            context.add_decision(Decision(
                id=f"D-{len(context.decisions)+1:03d}",
                status="adopted",
                decision=d.get("decision", ""),
                reason=d.get("reason", "Inferred default by Discovery")
            ))
            
        # Registrar Q-NN
        for d in data.get("user_decisions", []):
            context.add_decision(Decision(
                id=f"Q-{len(context.decisions)+1:03d}",
                status="resolved",
                decision=d.get("decision", ""),
                reason=d.get("reason", "User explicitly decided")
            ))
        
        if data.get("missing_info_question"):
            context._discovery_data["missing_info_question"] = data.get("missing_info_question")
            context._discovery_data["question_count"] += 1
            logger.info(f"[DiscoveryAgent] Pergunta {q_count+1}/{self.max_questions}: {data.get('missing_info_question')}")
            return DiscoveryStatus.NEEDS_INPUT
            
        if "missing_info_question" in context._discovery_data:
            del context._discovery_data["missing_info_question"]
            
        if brain_instance:
            req = {"domain": context.domain or "data_engineering", "architecture": context.architecture_decision}
            req = brain_instance.apply_intelligent_defaults(req)
            context.architecture_decision = req.get("architecture", {})

        context.freeze_context()
        logger.info("[DiscoveryAgent] Discovery concluído com sucesso.")
        return DiscoveryStatus.COMPLETE
