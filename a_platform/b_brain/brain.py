import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class Brain:
    """
    O Cérebro da plataforma.
    Centraliza o conhecimento core da plataforma e o separa do contexto do projeto sendo gerado.
    """
    def __init__(self):
        self.knowledge_base = {
            "analytics": "Conhecimento sobre pipelines de dados, ETL/ELT e Data Warehousing.",
            "ecommerce": "Conhecimento sobre sistemas transacionais e de inventário."
        }
        self.rules = {
            "architecture": ["Separação de conceitos", "Alta coesão", "Baixo acoplamento"],
            "security": ["Criptografia at-rest", "Princípio do Menor Privilégio"]
        }
        self.patterns = {
            "api": "RESTful, GraphQL",
            "database": "Star Schema, Snowflake Schema"
        }

    def get_knowledge(self, domain: str) -> str:
        return self.knowledge_base.get(domain.lower(), "Conhecimento genérico de engenharia de software.")

    def get_rules(self, category: str) -> list:
        return self.rules.get(category, [])

    def get_patterns(self, layer: str) -> str:
        return self.patterns.get(layer, "Padrões arquiteturais padrão.")
