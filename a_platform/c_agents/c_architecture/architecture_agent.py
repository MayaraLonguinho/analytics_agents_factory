import logging
import json
import re
from typing import Dict, Any

from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.b_brain.brain import Brain
from a_platform.b_brain.g_graph.graph_builder import GraphBuilder
from a_platform.f_llm_gateway.gateway import LLMGateway

logger = logging.getLogger(__name__)

class ArchitectureAgent:
    """
    Consome o Discovery, o Profiling e o Brain. 
    Decide as tecnologias, estrutura e gera uma "Architecture Decision" real usando LLM.
    """
    def __init__(self, brain: Brain, graph_builder: GraphBuilder):
        self.brain = brain
        self.graph_builder = graph_builder
        self.gateway = LLMGateway()

    def generate_architecture(self, request: ProjectRequest) -> bool:
        logger.info("[ArchitectureAgent] Iniciando definição de arquitetura via LLM...")
        
        # 1. Recuperar Conhecimento do Brain
        domain = request.discovery_data.get("domain", "generic")
        brain_context = self.brain.retrieve_relevant_knowledge(domain)
        
        logger.info(f"[ArchitectureAgent] Conhecimento recuperado para o domínio '{domain}'")
        
        # 2. Gerar o Grafo de Contexto
        graph = self.graph_builder.build_graph(request)
        request.graph_representation = graph
        logger.info(f"[ArchitectureAgent] Grafo de contexto gerado com {len(graph['nodes'])} nós.")
        
        # 3. Invocar LLM para Decisão Arquitetural
        system_prompt = (
            "Você é o Architecture Agent, um arquiteto de software principal.\n"
            "Sua tarefa é definir a pilha de tecnologia e a arquitetura para o projeto com base nos dados do Discovery, no Perfil do Dataset e no Conhecimento da Plataforma (Brain).\n"
            "Retorne APENAS um JSON válido contendo as seguintes chaves:\n"
            "- core_stack (ex: Python 3.10, Node.js, etc)\n"
            "- database_technology (A tecnologia de banco de dados escolhida)\n"
            "- architecture_pattern (ex: Microservices, Monolith, Data Lakehouse, Event-Driven)\n"
            "- data_processing (ex: Pandas, Spark, dbt, SQLAlchemy)\n"
            "- rationale (Breve justificativa técnica da sua escolha)\n"
        )
        
        prompt = (
            f"Discovery Data: {json.dumps(request.discovery_data, ensure_ascii=False)}\n"
            f"Dataset Profile: {json.dumps(request.dataset_profile, ensure_ascii=False)}\n"
            f"Brain Context: {json.dumps(brain_context, ensure_ascii=False)}\n"
        )
        
        response = self.gateway.generate(prompt, system_prompt=system_prompt, model_preference="openai")
        
        if not response.get("success"):
            logger.error(f"[ArchitectureAgent] LLM falhou ao gerar arquitetura: {response.get('error')}")
            return False
            
        text = response.get("text", "")
        # Extrair JSON do retorno (tratando blocos markdown)
        json_str = text
        match = re.search(r'```(?:json)?(.*?)```', text, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
            
        try:
            decision = json.loads(json_str)
        except Exception as e:
            logger.error(f"[ArchitectureAgent] Falha ao parsear JSON do LLM: {e}\nRetorno: {text}")
            return False
            
        decision["status"] = "APPROVED"
        decision["rules_applied"] = brain_context.get("architecture_rules", [])
        
        request.architecture_decision = decision
        
        # Injeta a decisão de volta no Brain para os próximos agentes
        self.brain.inject_project_context(request.project_id, "architecture", decision)
        
        # Regera o grafo para incluir o nó da arquitetura agora decidido
        graph = self.graph_builder.build_graph(request)
        request.graph_representation = graph
        
        logger.info(f"[ArchitectureAgent] Decisão arquitetural concluída: {decision.get('architecture_pattern')} com {decision.get('data_processing')}.")
        return True
