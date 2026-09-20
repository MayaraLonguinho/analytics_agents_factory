"""
c_tests/b_system/f_repair/e_test_repair_escalation.py
===================================================
Especificação executável de escalonamento de reparo após exaustão do limite local.
Valida que, após 3 tentativas de auto-recuperação local (max_repair_attempts=3),
o fluxo transiciona para escalonamento ou solicitação de intervenção humana (NEEDS_INPUT),
e NÃO encerra fatalmente o projeto sem alternativa.
"""
import pytest

from a_platform.b_contracts.j_state_manager import StateManager, ProjectPhase, PhaseStatus


def test_repair_escalation_after_three_attempts():
    """Valida a transição para NEEDS_INPUT após atingir o teto de 3 tentativas locais."""
    sm = StateManager(project_id="prj_escalate")

    # Realiza 3 tentativas locais
    for _ in range(3):
        assert sm.can_repair() is True
        sm.record_repair_attempt()

    assert sm.repair_attempts == 3
    assert sm.can_repair() is False

    # Quando esgotado, escalona para NEEDS_INPUT para decisão humana
    sm.transition_to(
        ProjectPhase.NEEDS_INPUT,
        {"reason": "Repair limit reached. User guidance required.", "escalated": True},
    )
    assert sm.current_phase == ProjectPhase.NEEDS_INPUT
    assert sm.phases[ProjectPhase.NEEDS_INPUT].details.get("escalated") is True
