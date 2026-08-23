import logging
from typing import Dict, Any
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.b_brain.brain import Brain
from a_platform.b_brain.g_graph.graph_builder import GraphBuilder

logger = logging.getLogger(__name__)

class ArchitectureAgent:
    """
    Consome o Discovery, o Profiling e o Brain. 
    Decide as tecnologias, estrutura e gera uma "Architecture Decision".
    """
    def __init__(self, brain: Brain, graph_builder: GraphBuilder):
        self.brain = brain
        self.graph_builder = graph_builder

    def generate_architecture(self, request: ProjectRequest) -> bool:
        logger.info("Iniciando Architecture Agent...")
        
        # 1. Recuperar Conhecimento do Brain
        domain = request.discovery_data.get("domain", "generic")
        db_choice = request.discovery_data.get("database", "Relacional Genérico")
        
        knowledge = self.brain.get_knowledge(domain)
        arch_rules = self.brain.get_rules("architecture")
        db_patterns = self.brain.get_patterns("database")
        
        logger.info(f"Conhecimento recuperado para o domínio '{domain}'")
        
        # 2. Gerar o Grafo de Contexto
        graph = self.graph_builder.build_graph(request)
        request.graph_representation = graph
        logger.info(f"Grafo de contexto gerado com {len(graph['nodes'])} nós e {len(graph['edges'])} arestas.")
        
        # 3. Decisões Dinâmicas baseadas no Dataset Profiling e Discovery
        has_large_dataset = False
        if request.dataset_profile and request.dataset_profile.get("row_count", 0) > 1000000:
            has_large_dataset = True
            
        decision = {
            "core_stack": "Python 3.10+",
            "database_technology": db_choice,
            "architecture_pattern": "Microservices" if has_large_dataset else "Monolith",
            "data_processing": "Spark/Databricks" if has_large_dataset else "Pandas/DuckDB",
            "rules_applied": arch_rules,
            "brain_context": knowledge,
            "database_patterns": db_patterns,
            "status": "APPROVED"
        }
        
        request.architecture_decision = decision
        logger.info(f"Decisão arquitetural concluída: {decision['architecture_pattern']} com {decision['data_processing']}.")
        
        return True
