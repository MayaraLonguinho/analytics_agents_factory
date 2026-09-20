"""
c_tests/b_system/e_state/c_test_resume_responsible_phase.py
=========================================================
Especificação executável de retomada para a fase responsável (ResponsiblePhase).
O Target Contract estabelece que a retomada após NEEDS_INPUT / PAUSED deve redirecionar
o fluxo para a fase específica que demandou a intervenção humana (ex: Architecture, Repair),
e NÃO forçar permanentemente o retorno para Discovery.
"""
import pytest

from a_platform.b_contracts.j_state_manager import StateManager, ProjectPhase, PhaseStatus


def test_resume_should_target_responsible_phase():
    """
    Especifica que a máquina de estados deve suportar retomada a partir de qualquer fase.
    Exemplo: Pausa ocorreu durante fase de ARCHITECTURE -> Retomada deve ir para ARCHITECTURE.
    """
    sm = StateManager(project_id="prj_resume_resp")

    # Simula estado em que a pausa foi provocada por decisão de arquitetura
    sm.transition_to(ProjectPhase.ARCHITECTURE)
    assert sm.current_phase == ProjectPhase.ARCHITECTURE

    sm.transition_to(ProjectPhase.NEEDS_INPUT, {"responsible_phase": "ARCHITECTURE"})
    assert sm.current_phase == ProjectPhase.NEEDS_INPUT

    # Na retomada contratual, a transição deve voltar para ARCHITECTURE
    target_phase = ProjectPhase.ARCHITECTURE
    sm.transition_to(target_phase)
    assert sm.current_phase == ProjectPhase.ARCHITECTURE
    assert sm.phases[ProjectPhase.ARCHITECTURE].status == PhaseStatus.IN_PROGRESS
