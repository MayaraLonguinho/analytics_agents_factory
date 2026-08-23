import yaml
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DomainRegistry:
    def __init__(self, registry_path: str = None):
        if registry_path is None:
            registry_path = os.path.join(os.path.dirname(__file__), "registry.yaml")
        
        self.registry_path = registry_path
        self.domains = {}
        self._load_registry()

    def _load_registry(self):
        try:
            with open(self.registry_path, 'r') as f:
                data = yaml.safe_load(f)
                self.domains = data.get("domains", {})
                logger.info(f"Carregados {len(self.domains)} domínios do registry.")
        except Exception as e:
            logger.error(f"Erro ao carregar registry de domínios: {e}")

    def get_domain_config(self, domain_name: str) -> Dict[str, Any]:
        domain_name = domain_name.lower().strip()
        if domain_name in self.domains:
            return self.domains[domain_name]
        logger.warning(f"Domínio '{domain_name}' não encontrado. Usando 'generic'.")
        return self.domains.get("generic", {
            "description": "Generic fallback",
            "agents": ["backend_agent"],
            "skills": ["basic_coding"],
            "mcps": ["filesystem_mcp"],
            "materializers": ["generic_materializer"]
        })
