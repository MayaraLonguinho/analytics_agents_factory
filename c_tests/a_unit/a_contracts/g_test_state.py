"""
c_tests/a_unit/a_contracts/g_test_state.py
========================================
Especificação executável do contrato StateManager, ProjectPhase e PhaseStatus.
Valida transições de fases, tracking de reparo, e persistência de checkpoints.
"""
import pytest

from a_platform.b_contracts.j_state_manager import (
    StateManager,
    ProjectPhase,
    PhaseStatus,
)


def test_state_manager_initialization():
    """Valida a inicialização da máquina de estados em ProjectPhase.INIT."""
    sm = StateManager(project_id="prj_state_1")
    assert sm.project_id == "prj_state_1"
    assert sm.current_phase == ProjectPhase.INIT
    assert sm.project_ready is False
    assert sm.repair_attempts == 0
    assert sm.max_repair_attempts == 3
    assert sm.phases[ProjectPhase.INIT].status == PhaseStatus.COMPLETED


def test_state_manager_transition_to_discovery():
    """Valida a transição de fase atualizando o status para IN_PROGRESS."""
    sm = StateManager(project_id="prj_state_2")
    sm.transition_to(ProjectPhase.DISCOVERY, {"intent": "ETL"})
    assert sm.current_phase == ProjectPhase.DISCOVERY
    assert sm.phases[ProjectPhase.DISCOVERY].status == PhaseStatus.IN_PROGRESS
    assert sm.phases[ProjectPhase.DISCOVERY].details.get("intent") == "ETL"


def test_state_manager_complete_phase():
    """Valida a conclusão explícita de uma fase com registro de detalhes."""
    sm = StateManager(project_id="prj_state_3")
    sm.transition_to(ProjectPhase.DISCOVERY)
    sm.complete_phase(ProjectPhase.DISCOVERY, {"domain": "analytics"})
    assert sm.phases[ProjectPhase.DISCOVERY].status == PhaseStatus.COMPLETED
    assert sm.phases[ProjectPhase.DISCOVERY].details.get("domain") == "analytics"


def test_state_manager_repair_increment():
    """Valida o incremento e verificação do limite de tentativas de reparo."""
    sm = StateManager(project_id="prj_state_4")
    assert sm.can_repair() is True
    assert sm.record_repair_attempt() == 1
    assert sm.record_repair_attempt() == 2
    assert sm.record_repair_attempt() == 3
    assert sm.can_repair() is False
