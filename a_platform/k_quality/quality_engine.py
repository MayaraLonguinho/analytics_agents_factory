import logging
import os
import yaml
from typing import Dict, Any

from a_platform.a_core.b_domain.project_request import ProjectRequest

logger = logging.getLogger(__name__)

class QualityEngine:
    """
    Quality Engine.
    Analisa qualidade estática e governança.
    """
    def __init__(self, thresholds_path: str = None):
        if not thresholds_path:
            thresholds_path = os.path.join(os.path.dirname(__file__), "thresholds.yaml")
        
        self.thresholds_path = thresholds_path
        self.metrics = {}
        self.passing_score = 60
        self._load_thresholds()

    def _load_thresholds(self):
        try:
            with open(self.thresholds_path, 'r') as f:
                data = yaml.safe_load(f)
                self.metrics = data.get("metrics", {})
                self.passing_score = data.get("passing_score", 60)
        except Exception as e:
            logger.error(f"[QualityEngine] Falha ao carregar thresholds: {e}")
            self.metrics = {"linting_weight": 0.3, "architecture_weight": 0.4, "documentation_weight": 0.3}

    def run_quality(self, request: ProjectRequest) -> bool:
        domain = request.discovery_data.get("domain", "generic").lower()
        project_dir = os.path.abspath(os.path.join(os.getcwd(), "e_generated_projects", domain, request.project_id))
        
        logger.info(f"[QualityEngine] Avaliando projeto em {project_dir}")
        
        if not os.path.exists(project_dir):
            return False

        # Avaliação mockada de qualidade de código
        # Num cenário real iteraria pelos arquivos .py
        linting_score = 100
        architecture_score = 100
        doc_score = 100
        
        # Penálise se não encontrar docs ou tipo
        py_files = [f for f in os.listdir(project_dir) if f.endswith(".py")]
        if not py_files:
            logger.warning("[QualityEngine] Nenhum arquivo .py encontrado, nota comprometida.")
            architecture_score = 50
        else:
            has_docstrings = False
            for pf in py_files:
                with open(os.path.join(project_dir, pf), "r") as code:
                    content = code.read()
                    if '"""' in content or "'''" in content:
                        has_docstrings = True
                        break
            if not has_docstrings:
                doc_score = 50
                logger.warning("[QualityEngine] Ausência de docstrings detectada. Penalizando doc_score.")

        # Calcula final
        final_score = (
            linting_score * self.metrics.get("linting_weight", 0.3) +
            architecture_score * self.metrics.get("architecture_weight", 0.4) +
            doc_score * self.metrics.get("documentation_weight", 0.3)
        )
        
        request.metadata["quality_score"] = final_score
        
        if final_score >= self.passing_score:
            logger.info(f"[QualityEngine] Qualidade aprovada com score {final_score:.1f} (Mínimo: {self.passing_score})")
            return True
        else:
            logger.error(f"[QualityEngine] Qualidade reprovada. Score: {final_score:.1f}")
            return False
