import logging
from a_platform.a_core.c_orchestration.state_manager import StateManager, ProjectPhase, PhaseStatus

logger = logging.getLogger(__name__)

class ReadinessGate:
    """
    Portão Absoluto de Prontidão do Projeto.
    Um projeto só pode ser declarado 'READY' se e somente se
    TODAS as fases críticas estiverem COMPLETED (e não falharam).
    Nenhum componente isolado (ou apenas build/arquivos passando) pode burlar essa regra.
    """
    
    # Fases que são estritamente obrigatórias para o sucesso de um projeto
    MANDATORY_PHASES = [
        ProjectPhase.DISCOVERY,
        ProjectPhase.PLANNER,
        ProjectPhase.MATERIALIZATION,
        ProjectPhase.EXECUTION,
        ProjectPhase.VALIDATION,
        ProjectPhase.QUALITY,
        ProjectPhase.CERTIFICATION
    ]

    @classmethod
    def evaluate(cls, state_manager: StateManager) -> bool:
        logger.info("[ReadinessGate] Avaliando métricas finais do projeto...")
        
        for phase in cls.MANDATORY_PHASES:
            status = state_manager.phases[phase].status
            if status != PhaseStatus.COMPLETED:
                logger.error(f"[ReadinessGate] ❌ Projeto não está pronto. A fase {phase.name} está com status {status.name}.")
                return False
                
        logger.info("[ReadinessGate] ✅ Todas as fases mandatórias foram completadas com sucesso.")
        return True
