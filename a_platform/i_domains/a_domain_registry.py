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

    def normalize_domain(self, domain_name: str) -> str:
        if not domain_name:
            # Fallback to analytics if nothing is provided
            return "analytics"
            
        domain_name = domain_name.lower().strip()
        
        # Mapeamento estrito de intenções equivalentes a ETL/Data Engineering
        de_aliases = {
            "etl", "etl pipeline", "data pipeline", "pipeline de dados",
            "data engineering", "engenharia de dados", "pipeline de ingestão",
            "pipeline de transformação", "pipeline de carga",
            "ingestão transformação carga", "extract transform load",
            "extract-transform-load"
        }
        if domain_name in de_aliases:
            return "data_engineering"
            
        an_aliases = {
            "analytics", "data analytics", "análise de dados", "dashboard",
            "bi", "business intelligence"
        }
        if domain_name in an_aliases:
            return "analytics"
            
        # Business contexts that are NOT domains
        # We enforce "analytics" as the default technical domain for these contexts
        business_contexts = {
            "sales", "finance", "hr", "inventory", "marketing", "logistics", 
            "clients", "personal_finance", "crm", "ecommerce", "erp"
        }
        if domain_name in business_contexts:
            logger.info(f"'{domain_name}' identificado como Business Context. Assumindo domínio técnico 'analytics'.")
            return "analytics"
            
        # Se for totalmente desconhecido, falha fallback seguro para analytics
        logger.warning(f"Domínio/Contexto '{domain_name}' não mapeado. Assumindo fallback 'analytics'.")
        return "analytics"

    def get_domain_config(self, domain_name: str) -> Dict[str, Any]:
        domain_name = self.normalize_domain(domain_name)
        if domain_name in self.domains:
            return self.domains[domain_name]
            
        logger.error(f"Domínio '{domain_name}' não encontrado no registry.yaml.")
        raise ValueError(f"Domínio '{domain_name}' estritamente não suportado pela Factory.")
