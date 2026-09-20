"""
c_tests/b_system/e_state/b_test_pause_resume.py
=============================================
Especificação executável de pausa e retomada de sessão (PAUSED -> USER ANSWER -> RESUME).
Valida o congelamento do estado quando uma pergunta está pendente e o registro
da resposta do usuário no histórico do contexto.
"""
from pathlib import Path
import pytest

from a_platform.b_contracts.j_state_manager import StateManager, ProjectPhase, PhaseStatus
from a_platform.b_contracts.i_execution_context import ExecutionContext


def test_pause_on_needs_input_and_resume_records_answer(tmp_path: Path):
    """Valida a transição para NEEDS_INPUT / PAUSED e a retomada com registro da resposta."""
    project_id = "prj_pause_resume"
    sm = StateManager(project_id=project_id)
    sm.state_dir = str(tmp_path)

    # 1. Transição para NEEDS_INPUT
    sm.transition_to(ProjectPhase.NEEDS_INPUT, {"pending_question": "Qual é o banco desejado?"})
    assert sm.current_phase == ProjectPhase.NEEDS_INPUT

    # 2. Resposta do usuário
    ctx = ExecutionContext(project_id=project_id)
    ctx.discovery_data["history"] = [
        {"role": "agent", "content": "Qual é o banco desejado?"},
        {"role": "user", "content": "PostgreSQL"},
    ]

    # 3. Retomada
    sm.complete_phase(ProjectPhase.NEEDS_INPUT)
    assert sm.phases[ProjectPhase.NEEDS_INPUT].status == PhaseStatus.COMPLETED
    assert len(ctx.discovery_data["history"]) == 2
    assert ctx.discovery_data["history"][1]["content"] == "PostgreSQL"
