import logging
import os
from typing import Dict, Any

from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.c_orchestration.state_manager import StateManager, ProjectPhase, PhaseStatus

logger = logging.getLogger(__name__)

class CertificationEngine:
    """
    Motor de Certificação.
    Avalia as evidências de todas as fases anteriores e aplica o Tier/Selo final.
    Gere um relatório auditável (CERTIFICATION.md).
    """
    def __init__(self):
        pass

    def run_certification(self, request: ProjectRequest, state_manager: StateManager = None) -> bool:
        logger.info("[CertificationEngine] Iniciando processo de certificação auditável...")
        
        # Se Validation ou Quality falharam, Certification falha imediatamente.
        if state_manager:
            val_status = state_manager.phases[ProjectPhase.VALIDATION].status
            qual_status = state_manager.phases[ProjectPhase.QUALITY].status
            
            if val_status == PhaseStatus.FAILED or qual_status == PhaseStatus.FAILED:
                logger.error("[CertificationEngine] Projeto reprovado porque Validation ou Quality falharam.")
                self._write_certification_stamp(request, "FAILED", 0.0, state_manager, False)
                return False
                
        score = request.metadata.get("quality_score", 0.0)
        
        if score < 60:
            logger.error("[CertificationEngine] Quality Score muito baixo.")
            self._write_certification_stamp(request, "FAILED", score, state_manager, False)
            return False
            
        tier = self._calculate_tier(score)
        request.metadata["certification_tier"] = tier
        
        logger.info(f"[CertificationEngine] Projeto certificado com o selo: {tier} (Score: {score:.1f})")
        
        self._write_certification_stamp(request, tier, score, state_manager, True)
        return True

    def _calculate_tier(self, score: float) -> str:
        if score >= 90:
            return "PLATINUM"
        elif score >= 70:
            return "GOLD"
        else:
            return "SILVER"

    def _write_certification_stamp(self, request: ProjectRequest, tier: str, score: float, state_manager: StateManager, success: bool):
        domain = request.discovery_data.get("domain", "generic").lower()
        stamp_path = os.path.join(os.getcwd(), "e_generated_projects", domain, request.project_id, "CERTIFICATION.md")
        
        try:
            os.makedirs(os.path.dirname(stamp_path), exist_ok=True)
            content = f"# Certificação Auditável do Projeto: {request.project_id}\n\n"
            content += f"## Veredito Final: {'✅ APROVADO' if success else '❌ REPROVADO'}\n"
            content += f"- **Selo (Tier)**: {tier}\n"
            content += f"- **Score Global (Quality)**: {score:.1f}\n"
            content += f"- **Tentativas de Reparo**: {request.metadata.get('repair_attempts', 0)}/3\n\n"
            
            content += "## Status dos Portões (Gates)\n"
            if state_manager:
                for phase in [ProjectPhase.DISCOVERY, ProjectPhase.PLANNER, ProjectPhase.MATERIALIZATION, 
                              ProjectPhase.EXECUTION, ProjectPhase.VALIDATION, ProjectPhase.QUALITY]:
                    status = state_manager.phases[phase].status.name
                    emoji = "🟢" if status == "COMPLETED" else "🔴" if status == "FAILED" else "⚪"
                    content += f"- {phase.name}: {emoji} {status}\n"
            else:
                content += "*(Dados de orquestração indisponíveis)*\n"
                
            content += "\n*Documento gerado automaticamente pela Analytics Agents Factory (A.A.F.).*\n"
            
            with open(stamp_path, "w") as f:
                f.write(content)
                
        except Exception as e:
            logger.warning(f"[CertificationEngine] Falha ao escrever o relatório de certificação no disco: {e}")
