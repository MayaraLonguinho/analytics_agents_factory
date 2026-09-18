import logging
import json
import re
from enum import Enum, auto
from typing import Any

from a_platform.b_contracts.e_execution_context import ExecutionContext, Decision
from a_platform.i_llm_gateway.d_gateway import LLMGateway

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
        
        # Garantir estrutura canônica de discovery_data serializável no ExecutionContext
        if not hasattr(context, "discovery_data") or context.discovery_data is None:
            context.discovery_data = {}
            
        if "history" not in context.discovery_data:
            context.discovery_data["history"] = []
        if "question_count" not in context.discovery_data:
            context.discovery_data["question_count"] = 0
            
        history = context.discovery_data.get("history", [])
        q_count = context.discovery_data.get("question_count", 0)
        
        # Checagem de limite de orçamento de perguntas
        if q_count >= self.max_questions:
            logger.info("[DiscoveryAgent] Limite de perguntas atingido. Congelando com defaults do Brain.")
            if brain_instance:
                req = {"domain": context.domain or "data_engineering", "architecture": context.architecture_decision}
                req = brain_instance.apply_intelligent_defaults(req)
                context.architecture_decision = req.get("architecture", {})
            
            context.add_decision(Decision(
                id=f"D-DISC-00{len(context.decisions)+1}",
                status="adopted",
                decision="Assumed intelligent defaults due to max questions limit.",
                reason="Max discovery questions reached."
            ))
            context.discovery_data["pending_question"] = None
            context.freeze_context()
            return DiscoveryStatus.COMPLETE

        dataset_clause = ""
        if context.dataset_path:
            dataset_clause = (
                f"\nNOTA SOBRE O DATASET FORNECIDO ('{context.dataset_path}'):\n"
                "- A etapa subsequente de Dataset Profiling inspecionará o arquivo fisicamente (linhas, colunas, schema, tipos e duplicatas).\n"
                "- É ESTRITAMENTE PROIBIDO fazer perguntas sobre propriedades físicas do dataset (contagem de linhas/colunas, nomes brutos de campos, duplicatas, delimitadores óbvios).\n"
            )

        system_prompt = (
            "Você é o Discovery Agent da Analytics Agents Factory (AAF).\n"
            "Sua tarefa é mapear os requisitos arquiteturais e de negócio do projeto de analytics ou data engineering.\n"
            f"{dataset_clause}"
            "REGRAS CRÍTICAS DE PROTOCOLO:\n"
            "1. Você pode fazer no MÁXIMO UMA pergunta por vez ao usuário.\n"
            "2. Orçamento MÁXIMO DE 5 PERGUNTAS ao longo de toda a sessão.\n"
            "3. Pergunte SOMENTE se a resposta alterar arquitetura, escopo, capability, fonte, destino ou critério de aceite, ou quando existir ambiguidade semântica que não possa ser resolvida deterministicamente.\n"
            "4. NÃO faça perguntas desnecessárias sobre propriedades físicas que o profiler descobre no arquivo fornecido.\n"
            "5. Se os requisitos essenciais já estiverem claros ou puderem ser atendidos pelos padrões técnicos da fábrica (ex: SQLite local, Python puro, sanitização padrão), assuma defaults inteligentes (assumed_defaults) e defina missing_info_question como null.\n"
            "6. Toda decisão relevante assumida DEVE gerar um ID D-NNN explícito no retorno (ex: D-001: Assumir SQLite local).\n"
            "7. Toda questão pendente resolvida ou solicitada DEVE gerar um ID Q-NNN explícito.\n"
            "Extraia obrigatoriamente: project_type, business_context, domain.\n"
            "Retorne APENAS um JSON válido no formato:\n"
            "{\n"
            '  "project_type": "...",\n'
            '  "business_context": "...",\n'
            '  "domain": "...",\n'
            '  "assumed_defaults": [{"id": "D-001", "decision": "...", "reason": "..."}],\n'
            '  "user_decisions": [{"id": "Q-001", "decision": "...", "reason": "..."}],\n'
            '  "missing_info_question": "Pergunta se for crítico, senão null"\n'
            "}"
        )
        
        prompt = f"Prompt Original: {context.prompt}\nHistórico da Conversa: {json.dumps(history, ensure_ascii=False)}\nPerguntas feitas: {q_count}/{self.max_questions}\n{system_prompt}"
        
        schema = {
            "type": "object",
            "properties": {
                "project_type": {"type": "string"},
                "business_context": {"type": "string"},
                "domain": {"type": "string"},
                "assumed_defaults": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "decision": {"type": "string"},
                            "reason": {"type": "string"}
                        }
                    }
                },
                "user_decisions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "decision": {"type": "string"},
                            "reason": {"type": "string"}
                        }
                    }
                },
                "missing_info_question": {"type": ["string", "null"]}
            },
            "required": ["project_type", "business_context", "domain"]
        }
        
        try:
            response = await self.gateway.structured_output(prompt, schema)
            if not response or not response.content:
                logger.error("[DiscoveryAgent] Resposta vazia ou nula recebida do LLM Gateway.")
                return DiscoveryStatus.FAILED
            data = json.loads(response.content)
        except Exception as e:
            logger.error(f"[DiscoveryAgent] Falha ao obter output estruturado do LLM: {e}")
            return DiscoveryStatus.FAILED
            
        if data.get("project_type"):
            context.project_type = data.get("project_type")
            context.discovery_data["project_type"] = data.get("project_type")
        if data.get("business_context"):
            context.business_context = data.get("business_context")
            context.discovery_data["business_context"] = data.get("business_context")
        if data.get("domain"):
            context.domain = data.get("domain")
            context.discovery_data["domain"] = data.get("domain")
        
        # Registrar D-NNN
        for d in data.get("assumed_defaults", []):
            decision_id = d.get("id", f"D-{len(context.decisions)+1:03d}")
            context.add_decision(Decision(
                id=decision_id,
                status="adopted",
                decision=d.get("decision", ""),
                reason=d.get("reason", "Inferred default by Discovery")
            ))
            
        # Registrar Q-NNN
        for d in data.get("user_decisions", []):
            decision_id = d.get("id", f"Q-{len(context.decisions)+1:03d}")
            context.add_decision(Decision(
                id=decision_id,
                status="resolved",
                decision=d.get("decision", ""),
                reason=d.get("reason", "User explicitly decided")
            ))
        
        missing_q = data.get("missing_info_question")
        if missing_q:
            context.discovery_data["pending_question"] = missing_q
            context.discovery_data["question_count"] = q_count + 1
            context.discovery_data["history"].append({
                "role": "agent",
                "content": missing_q
            })
            logger.info(f"[DiscoveryAgent] Pergunta {context.discovery_data['question_count']}/{self.max_questions}: {missing_q}")
            return DiscoveryStatus.NEEDS_INPUT
            
        context.discovery_data["pending_question"] = None
            
        if brain_instance:
            req = {"domain": context.domain or "data_engineering", "architecture": context.architecture_decision}
            req = brain_instance.apply_intelligent_defaults(req)
            context.architecture_decision = req.get("architecture", {})

        context.freeze_context()
        logger.info("[DiscoveryAgent] Discovery concluído com sucesso.")
        return DiscoveryStatus.COMPLETE
