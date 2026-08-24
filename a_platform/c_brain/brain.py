import logging
from typing import Dict, Any, List

from a_platform.b_brain.f_registry.knowledge_registry import KnowledgeRegistry
from a_platform.b_brain.f_registry.rule_registry import RuleRegistry
from a_platform.b_brain.f_registry.pattern_registry import PatternRegistry

logger = logging.getLogger(__name__)

class Brain:
    """
    O Cérebro da plataforma.
    Centraliza o conhecimento core da plataforma (regras fixas) 
    e gerencia o conhecimento de projetos (dinâmico) através de registries formais.
    """
    def __init__(self):
        self.knowledge_registry = KnowledgeRegistry()
        self.rule_registry = RuleRegistry()
        self.pattern_registry = PatternRegistry()
        
        self._initialize_core_knowledge()
        self._initialize_core_rules()
        self._initialize_core_patterns()
        
        # Project Knowledge (armazenado por contexto da execução atual ou memória passada)
        self.project_knowledge = {}

    def _initialize_core_knowledge(self):
        self.knowledge_registry.register("db_support", {
            "supported_databases": ["PostgreSQL", "MongoDB", "SQLite", "DuckDB", "Snowflake", "BigQuery"],
            "domain": "platform",
            "tags": ["database", "core"]
        })
        self.knowledge_registry.register("lang_support", {
            "supported_languages": ["Python 3.10+", "SQL", "JavaScript", "TypeScript"],
            "domain": "platform",
            "tags": ["language", "core"]
        })
        self.knowledge_registry.register("arch_core", {
            "core_architectures": {
                "monolith": "Ideal para sistemas de pequeno porte e MVPs.",
                "microservices": "Ideal para alta escalabilidade e equipes distribuídas.",
                "data_pipeline": "Ideal para Analytics, ETL/ELT."
            },
            "domain": "platform",
            "tags": ["architecture", "core"]
        })

    def _initialize_core_rules(self):
        self.rule_registry.register("arch_soc", {
            "rule": "Separação de conceitos (SoC).",
            "category": "architecture"
        })
        self.rule_registry.register("arch_cohesion", {
            "rule": "Alta coesão e Baixo acoplamento.",
            "category": "architecture"
        })
        self.rule_registry.register("arch_db_logic", {
            "rule": "Não utilize lógicas de negócio no banco de dados (evite procedures densas).",
            "category": "architecture"
        })
        self.rule_registry.register("sec_crypto", {
            "rule": "Criptografia at-rest para dados sensíveis.",
            "category": "security"
        })
        self.rule_registry.register("sec_privilege", {
            "rule": "Princípio do Menor Privilégio.",
            "category": "security"
        })

    def _initialize_core_patterns(self):
        self.pattern_registry.register("analytics_patterns", {
            "pattern": "Star Schema, ELT, Data Lakehouse",
            "domain": "analytics"
        })
        self.pattern_registry.register("ecommerce_patterns", {
            "pattern": "3-Tier Architecture, Event-Driven, ACID Compliance",
            "domain": "ecommerce"
        })

    def retrieve_relevant_knowledge(self, domain: str) -> Dict[str, Any]:
        """
        Retorna o contexto condensado e focado no domínio utilizando os Registries.
        """
        domain_lower = domain.lower()
        
        # Recupera tudo marcado como 'platform' do KnowledgeRegistry
        platform_kb = self.knowledge_registry.search_by_domain("platform")
        platform_stack = {}
        for kb in platform_kb:
            platform_stack.update({k: v for k, v in kb.items() if k not in ["domain", "tags"]})
        
        knowledge_context = {
            "platform_stack": platform_stack,
            "architecture_rules": self.get_rules("architecture"),
            "security_rules": self.get_rules("security")
        }
        
        # Extrai patterns baseados no domínio
        patterns = self.pattern_registry.search_by_domain(domain_lower)
        if patterns:
            knowledge_context["domain_patterns"] = f"Padrões recomendados: {patterns[0].get('pattern')}"
        else:
            knowledge_context["domain_patterns"] = "Padrões genéricos de engenharia de software."
            
        return knowledge_context

    def inject_project_context(self, project_id: str, key: str, value: Any):
        """Permite que os agentes alimentem o Brain com decisões do projeto."""
        if project_id not in self.project_knowledge:
            self.project_knowledge[project_id] = {}
        self.project_knowledge[project_id][key] = value

    def get_rules(self, category: str) -> list:
        rules = self.rule_registry.search_by_tags([category])
        return [r.get("rule") for r in rules]
