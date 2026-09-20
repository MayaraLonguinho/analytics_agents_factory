"""
c_tests/b_system/f_repair/d_test_reprocess_from_phase.py
======================================================
Especificação executável de reprocessamento a partir da fase responsável.
Valida que, após o reparo e a invalidação, a execução retoma da fase corrigida
e segue o Golden Path até a nova validação dos gates.
"""
import pytest

from a_platform.b_contracts.j_state_manager import StateManager, ProjectPhase, PhaseStatus


def test_reprocess_flow_from_planner():
    """Valida o reprocessamento iniciando no PLANNER após falha em task."""
    sm = StateManager(project_id="prj_reproc")
    sm.record_repair_attempt()

    # Transiciona de volta para o PLANNER
    sm.transition_to(ProjectPhase.PLANNER, {"repair_cycle": 1, "action": "replan"})
    assert sm.current_phase == ProjectPhase.PLANNER
    assert sm.phases[ProjectPhase.PLANNER].status == PhaseStatus.IN_PROGRESS
    assert sm.repair_attempts == 1

    # Conclui planner corrigido
    sm.complete_phase(ProjectPhase.PLANNER, {"repaired_plan": True})
    assert sm.phases[ProjectPhase.PLANNER].status == PhaseStatus.COMPLETED

    # Segue para FACTORY
    sm.transition_to(ProjectPhase.PROJECT_FACTORY)
    assert sm.current_phase == ProjectPhase.PROJECT_FACTORY
