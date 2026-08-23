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
                if not self.domains:
                    raise ValueError("Registry vazio ou estrutura 'domains' ausente.")
                logger.info(f"Carregados {len(self.domains)} domínios do registry.")
        except Exception as e:
            logger.error(f"Erro CRÍTICO ao carregar registry de domínios: {e}")
            raise RuntimeError(f"Falha na fundação AAF Core: Não foi possível carregar {self.registry_path}") from e

    def get_domain_config(self, domain_name: str) -> Dict[str, Any]:
        domain_name = domain_name.lower().strip()
        if domain_name in self.domains:
            return self.domains[domain_name]
            
        logger.error(f"Domínio '{domain_name}' não encontrado e fallback não é permitido.")
        raise ValueError(f"Domínio '{domain_name}' estritamente não suportado pela Factory.")
