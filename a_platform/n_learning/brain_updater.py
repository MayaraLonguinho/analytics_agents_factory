import os
import yaml
import logging
from dataclasses import dataclass, asdict
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

@dataclass
class KnowledgeItem:
    domain: str
    pattern: str
    recommendation: str

class BrainUpdater:
    """
    Atualiza e estrutura a base de conhecimento (KnowledgeRegistry)
    persistindo lições aprendidas em formato YAML no diretório do domínio.
    """
    def __init__(self):
        self.domains_path = os.path.join(
            os.path.dirname(__file__), "..", "b_brain", "a_knowledge", "domains"
        )
        
    def save_lesson(self, item: KnowledgeItem):
        domain = item.domain.lower()
        domain_dir = os.path.join(self.domains_path, domain)
        os.makedirs(domain_dir, exist_ok=True)
        
        file_path = os.path.join(domain_dir, "learned_rules.yaml")
        rules = []
        
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    data = yaml.safe_load(f)
                    if isinstance(data, list):
                        rules = data
                    elif isinstance(data, dict) and "rules" in data:
                        rules = data["rules"]
            except Exception as e:
                logger.warning(f"[BrainUpdater] Falha ao ler {file_path}: {e}")
        
        rules.append(asdict(item))
        
        try:
            with open(file_path, "w") as f:
                yaml.dump({"rules": rules}, f, default_flow_style=False, allow_unicode=True)
            logger.info(f"[BrainUpdater] Lição salva com sucesso em {file_path}")
        except Exception as e:
            logger.error(f"[BrainUpdater] Falha ao escrever lição em {file_path}: {e}")
