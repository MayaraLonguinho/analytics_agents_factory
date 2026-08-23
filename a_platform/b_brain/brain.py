import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class Brain:
    """
    O Cérebro da plataforma.
    Centraliza o conhecimento core da plataforma (regras fixas) 
    e gerencia o conhecimento de projetos (dinâmico).
    """
    def __init__(self):
        # Platform Knowledge (regras fixas, tecnologias suportadas)
        self.platform_knowledge = {
            "supported_databases": ["PostgreSQL", "MongoDB", "SQLite", "DuckDB", "Snowflake", "BigQuery"],
            "supported_languages": ["Python 3.10+", "SQL", "JavaScript", "TypeScript"],
            "core_architectures": {
                "monolith": "Ideal para sistemas de pequeno porte e MVPs.",
                "microservices": "Ideal para alta escalabilidade e equipes distribuídas.",
                "data_pipeline": "Ideal para Analytics, ETL/ELT."
            }
        }
        
        self.platform_rules = {
            "architecture": [
                "Separação de conceitos (SoC).",
                "Alta coesão e Baixo acoplamento.",
                "Não utilize lógicas de negócio no banco de dados (evite procedures densas)."
            ],
            "security": [
                "Criptografia at-rest para dados sensíveis.",
                "Princípio do Menor Privilégio."
            ]
        }
        
        # Project Knowledge (armazenado por contexto da execução atual ou memória passada)
        self.project_knowledge = {}

    def retrieve_relevant_knowledge(self, domain: str) -> Dict[str, Any]:
        """
        Retorna o contexto condensado e focado no domínio.
        Pode ser expandido para utilizar um vetor (RAG) no futuro.
        """
        domain_lower = domain.lower()
        
        knowledge_context = {
            "platform_stack": self.platform_knowledge,
            "architecture_rules": self.platform_rules.get("architecture", []),
            "security_rules": self.platform_rules.get("security", [])
        }
        
        # Simula a extração de patterns do projeto
        if "analytics" in domain_lower or "data" in domain_lower:
            knowledge_context["domain_patterns"] = "Padrões recomendados: Star Schema, ELT, Data Lakehouse."
        elif "ecommerce" in domain_lower or "saas" in domain_lower:
            knowledge_context["domain_patterns"] = "Padrões recomendados: 3-Tier Architecture, Event-Driven, ACID Compliance."
        else:
            knowledge_context["domain_patterns"] = "Padrões genéricos de engenharia de software."
            
        return knowledge_context

    def inject_project_context(self, project_id: str, key: str, value: Any):
        """Permite que os agentes alimentem o Brain com decisões do projeto."""
        if project_id not in self.project_knowledge:
            self.project_knowledge[project_id] = {}
        self.project_knowledge[project_id][key] = value

    def get_rules(self, category: str) -> list:
        return self.platform_rules.get(category, [])
