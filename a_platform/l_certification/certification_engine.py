import logging
import os
from typing import Dict, Any

from a_platform.a_core.b_domain.project_request import ProjectRequest

logger = logging.getLogger(__name__)

class CertificationEngine:
    """
    Motor de Certificação.
    Aplica o Tier/Selo final no projeto (Silver, Gold, Platinum)
    baseado puramente no score gerado pela Quality Engine.
    """
    def __init__(self):
        pass

    def run_certification(self, request: ProjectRequest) -> bool:
        logger.info("[CertificationEngine] Iniciando processo de certificação...")
        
        score = request.metadata.get("quality_score")
        if score is None:
            logger.error("[CertificationEngine] 'quality_score' não encontrado no contexto. O QualityEngine rodou com sucesso?")
            return False
            
        tier = self._calculate_tier(score)
        request.metadata["certification_tier"] = tier
        
        logger.info(f"[CertificationEngine] Projeto certificado com o selo: {tier} (Score: {score:.1f})")
        
        self._write_certification_stamp(request, tier, score)
        return True

    def _calculate_tier(self, score: float) -> str:
        if score >= 90:
            return "PLATINUM"
        elif score >= 70:
            return "GOLD"
        else:
            return "SILVER"

    def _write_certification_stamp(self, request: ProjectRequest, tier: str, score: float):
        domain = request.discovery_data.get("domain", "generic").lower()
        stamp_path = os.path.join(os.getcwd(), "e_generated_projects", domain, request.project_id, "CERTIFICATION.md")
        
        try:
            content = f"# Certificação do Projeto: {request.project_id}\n\n"
            content += f"- **Tier**: {tier}\n"
            content += f"- **Score Global**: {score:.1f}\n"
            content += "\n*Projeto gerado e certificado pela Analytics Agents Factory.*\n"
            
            with open(stamp_path, "w") as f:
                f.write(content)
        except Exception as e:
            logger.warning(f"[CertificationEngine] Falha ao escrever o selo no disco: {e}")
