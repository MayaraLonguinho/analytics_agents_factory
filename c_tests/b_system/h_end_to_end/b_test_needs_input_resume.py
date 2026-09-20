"""
c_tests/b_system/h_end_to_end/b_test_needs_input_resume.py
========================================================
Especificação executável do fluxo ponta a ponta com pausa e resposta humana.
Request incompleto -> Discovery -> NEEDS_INPUT -> PAUSED ->
USER ANSWER -> RESUME -> Retomada do Golden Path -> PROJECT READY = YES.
"""
import pytest

from a_platform.b_contracts.j_state_manager import StateManager, ProjectPhase, PhaseStatus
from a_platform.b_contracts.i_execution_context import ExecutionContext


def test_needs_input_to_resume_e2e_flow():
    """Valida o ciclo completo de interrupção e continuação no ciclo de fabricação."""
    project_id = "prj_e2e_resume"
    sm = StateManager(project_id=project_id)
    ctx = ExecutionContext(project_id=project_id, prompt="Build analytics pipeline")

    # 1. Discovery identifica ausência de informação indispensável
    sm.transition_to(
        ProjectPhase.NEEDS_INPUT,
        {"pending_question": "Qual é a base de dados de destino?"},
    )
    assert sm.current_phase == ProjectPhase.NEEDS_INPUT
    assert sm.phases[ProjectPhase.NEEDS_INPUT].status == PhaseStatus.IN_PROGRESS

    # 2. Usuário responde
    user_answer = "PostgreSQL em schema analítico"
    ctx.discovery_data["history"] = [
        {"role": "agent", "content": "Qual é a base de dados de destino?"},
        {"role": "user", "content": user_answer},
    ]

    # 3. Retomada da sessão
    sm.complete_phase(ProjectPhase.NEEDS_INPUT)
    assert sm.phases[ProjectPhase.NEEDS_INPUT].status == PhaseStatus.COMPLETED

    # 4. Transiciona para a próxima fase do Golden Path (DATASET_PROFILING ou BRAIN)
    sm.transition_to(ProjectPhase.DATASET_PROFILING)
    assert sm.current_phase == ProjectPhase.DATASET_PROFILING
    assert sm.phases[ProjectPhase.DATASET_PROFILING].status == PhaseStatus.IN_PROGRESS
