import logging
from typing import Any
from a_platform.a_core.b_domain.project_request import ProjectRequest

logger = logging.getLogger(__name__)

class DiscoveryAgent:
    def __init__(self):
        self.required_fields = {
            "domain": "Qual é o domínio/assunto principal do projeto? (ex: Ecommerce, Finanças, Saúde)",
            "database": "Qual banco de dados devemos usar? (ex: PostgreSQL, MongoDB, SQLite)",
            "restrictions": "Existe alguma restrição técnica ou arquitetural? (ex: Apenas Python 3.10, Sem Docker, Nenhuma)"
        }

    def run_discovery(self, request: ProjectRequest) -> bool:
        logger.info("Iniciando Discovery Interativo...")
        
        if request.domain and "domain" not in request.discovery_data:
            request.discovery_data["domain"] = request.domain
            
        for field, question in self.required_fields.items():
            if field not in request.discovery_data or not request.discovery_data[field]:
                print(f"\n[DISCOVERY AGENT] 🔎 Precisamos de mais informações:")
                print(question)
                try:
                    answer = input("Resposta: ").strip()
                except EOFError:
                    answer = ""
                
                if not answer:
                    logger.error(f"O campo '{field}' é obrigatório para avançar.")
                    return False
                request.discovery_data[field] = answer

        request.discovery_data["status"] = "COMPLETE"
        logger.info("Discovery concluído com sucesso.")
        return True
