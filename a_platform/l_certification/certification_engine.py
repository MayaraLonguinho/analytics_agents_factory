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
        
        score = request.metadata.get("quality_score", 0.0)
        
        if state_manager:
            exec_status = state_manager.phases[ProjectPhase.EXECUTION].status
            val_status = state_manager.phases[ProjectPhase.VALIDATION].status
            qual_status = state_manager.phases[ProjectPhase.QUALITY].status
            
            if exec_status != PhaseStatus.COMPLETED or val_status != PhaseStatus.COMPLETED or qual_status != PhaseStatus.COMPLETED:
                logger.error("[CertificationEngine] Projeto reprovado porque Execution, Validation ou Quality falharam.")
                self._write_certification_stamp(request, "FAILED", score, state_manager, False)
                return False
                
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
            
            if state_manager:
                status_map = {
                    ProjectPhase.DISCOVERY: state_manager.phases[ProjectPhase.DISCOVERY].status.name,
                    ProjectPhase.PLANNER: state_manager.phases[ProjectPhase.PLANNER].status.name,
                    ProjectPhase.MATERIALIZATION: state_manager.phases[ProjectPhase.MATERIALIZATION].status.name,
                    ProjectPhase.EXECUTION: state_manager.phases[ProjectPhase.EXECUTION].status.name,
                    ProjectPhase.VALIDATION: state_manager.phases[ProjectPhase.VALIDATION].status.name,
                    ProjectPhase.QUALITY: state_manager.phases[ProjectPhase.QUALITY].status.name
                }
                def _to_pass_fail(s):
                    return "PASS" if s == "COMPLETED" else "FAIL"
            else:
                status_map = {}
                def _to_pass_fail(s):
                    return "UNKNOWN"
            
            disc_st = _to_pass_fail(status_map.get(ProjectPhase.DISCOVERY))
            plan_st = _to_pass_fail(status_map.get(ProjectPhase.PLANNER))
            mat_st = _to_pass_fail(status_map.get(ProjectPhase.MATERIALIZATION))
            exec_st = _to_pass_fail(status_map.get(ProjectPhase.EXECUTION))
            val_st = _to_pass_fail(status_map.get(ProjectPhase.VALIDATION))
            qual_st = _to_pass_fail(status_map.get(ProjectPhase.QUALITY))
            
            repair_attempts = request.metadata.get("repair_attempts", 0)
            
            content = f"# CERTIFICATION REPORT\n"
            content += f"- Project ID: {request.project_id}\n"
            content += f"- Domain: {domain}\n"
            content += f"- Discovery: {disc_st}\n"
            content += f"- Planning: {plan_st}\n"
            content += f"- Materialization: {mat_st}\n"
            content += f"- Execution: {exec_st}\n"
            content += f"- Validation: {val_st}\n"
            content += f"- Quality: {qual_st}\n"
            content += f"- Repair Attempts: {repair_attempts}\n"
            content += f"- Final Score: {score:.1f}\n"
            content += f"- Tier: {tier}\n"
            content += f"---\n"
            content += f"- VERDICT: {'CERTIFIED' if success else 'REJECTED'}\n"
            content += f"- PROJECT READY: {'YES' if success else 'NO'}\n"
            
            with open(stamp_path, "w") as f:
                f.write(content)
                
        except Exception as e:
            logger.warning(f"[CertificationEngine] Falha ao escrever o relatório de certificação no disco: {e}")
