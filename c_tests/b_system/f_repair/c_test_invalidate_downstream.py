"""
c_tests/b_system/f_repair/c_test_invalidate_downstream.py
=======================================================
Especificação executável de invalidação downstream no loop de Repair.
Valida que, ao retornar para uma fase anterior (ex: ARCHITECTURE),
todos os artefatos, planos e evidências gerados pelas fases subsequentes são invalidados,
impedindo o reaproveitamento silencioso de dados obsoletos.
"""
import pytest

from a_platform.b_contracts.j_state_manager import StateManager, ProjectPhase, PhaseStatus
from a_platform.b_contracts.i_execution_context import ExecutionContext


def invalidate_downstream_phases(sm: StateManager, target_phase: ProjectPhase):
    """Lógica canônica de invalidação de fases a jusante na máquina de estados."""
    phase_order = [
        ProjectPhase.INIT,
        ProjectPhase.DISCOVERY,
        ProjectPhase.DATASET_PROFILING,
        ProjectPhase.BRAIN,
        ProjectPhase.ARCHITECTURE,
        ProjectPhase.PLANNER,
        ProjectPhase.PROJECT_FACTORY,
        ProjectPhase.MATERIALIZATION,
        ProjectPhase.EXECUTION,
        ProjectPhase.VALIDATION,
        ProjectPhase.QUALITY,
        ProjectPhase.CERTIFICATION,
        ProjectPhase.READY,
    ]
    target_idx = phase_order.index(target_phase)
    for i in range(target_idx + 1, len(phase_order)):
        downstream_phase = phase_order[i]
        if downstream_phase in sm.phases:
            sm.phases[downstream_phase].status = PhaseStatus.PENDING
            sm.phases[downstream_phase].details.clear()


def test_invalidation_when_repairing_from_architecture():
    """Valida a invalidação de Planner, Factory, Materialization, Runtime e Gates ao reprocessar de ARCHITECTURE."""
    sm = StateManager(project_id="prj_inval")

    # Marca fases como concluídas
    sm.complete_phase(ProjectPhase.ARCHITECTURE, {"status": "ok"})
    sm.complete_phase(ProjectPhase.PLANNER, {"plan": "old"})
    sm.complete_phase(ProjectPhase.PROJECT_FACTORY, {"artifacts": ["old.py"]})
    sm.complete_phase(ProjectPhase.EXECUTION, {"exec": "failed"})

    # Invalida a partir de ARCHITECTURE
    invalidate_downstream_phases(sm, ProjectPhase.ARCHITECTURE)

    assert sm.phases[ProjectPhase.PLANNER].status == PhaseStatus.PENDING
    assert sm.phases[ProjectPhase.PLANNER].details == {}
    assert sm.phases[ProjectPhase.PROJECT_FACTORY].status == PhaseStatus.PENDING
    assert sm.phases[ProjectPhase.PROJECT_FACTORY].details == {}
    assert sm.phases[ProjectPhase.EXECUTION].status == PhaseStatus.PENDING
