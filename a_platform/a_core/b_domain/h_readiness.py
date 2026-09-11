import logging
from typing import Dict, Any, Optional
from a_platform.a_core.c_orchestration.c_state_manager import StateManager, ProjectPhase, PhaseStatus

from a_platform.j_runtime.c_runtime import ExecutionResult
from a_platform.k_validation.a_validation_gate import ValidationReport
from a_platform.l_quality.b_quality_engine import QualityReport
from a_platform.m_certification.a_certification_engine import CertificationResult

logger = logging.getLogger(__name__)

class ReadinessGate:
    """
    Portão Absoluto de Prontidão do Projeto.
    Um projeto só pode ser declarado 'READY' se e somente se
    TODAS as fases críticas tiverem evidências estritas de sucesso.
    """
    
    @classmethod
    def evaluate(
        cls, 
        state_manager: StateManager,
        execution_result: Optional[ExecutionResult] = None,
        validation_result: Optional[ValidationReport] = None,
        quality_result: Optional[QualityReport] = None,
        certification_result: Optional[CertificationResult] = None
    ) -> bool:
        logger.info("[ReadinessGate] Avaliando métricas finais e evidências reais do projeto...")
        
        # 1. Checagem de Orquestração (Discovery e Planning)
        if state_manager.phases[ProjectPhase.DISCOVERY].status != PhaseStatus.COMPLETED:
            logger.error("[ReadinessGate] ❌ Projeto não está pronto. Discovery não está COMPLETE.")
            return False
            
        if state_manager.phases[ProjectPhase.PLANNER].status != PhaseStatus.COMPLETED:
            logger.error("[ReadinessGate] ❌ Projeto não está pronto. Planning não está COMPLETE.")
            return False
            
        if state_manager.phases[ProjectPhase.MATERIALIZATION].status != PhaseStatus.COMPLETED:
            logger.error("[ReadinessGate] ❌ Projeto não está pronto. Materialization não está COMPLETE.")
            return False

        # 2. Checagem de Evidências Reais
        if not execution_result or execution_result.status != "SUCCESS":
            logger.error(f"[ReadinessGate] ❌ Projeto não está pronto. Execution FAIL. ({getattr(execution_result, 'status', 'None')})")
            return False
            
        if not validation_result or not validation_result.passed:
            logger.error("[ReadinessGate] ❌ Projeto não está pronto. Validation FAIL.")
            return False
            
        if not quality_result or not quality_result.passed:
            logger.error("[ReadinessGate] ❌ Projeto não está pronto. Quality FAIL.")
            return False
            
        if not certification_result or not certification_result.passed:
            logger.error("[ReadinessGate] ❌ Projeto não está pronto. Certification FAIL.")
            return False
            
        logger.info("[ReadinessGate] ✅ Todas as fases e evidências foram confirmadas com sucesso. PROJECT READY = YES")
        return True
