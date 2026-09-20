"""
c_tests/b_system/g_interfaces/b_test_resume.py
============================================
Especificação executável da interface pública de retomada de projetos (resume).
Valida que o boundary de aplicação recebe project_id e resposta do usuário,
descongela o contexto e dá continuidade ao fluxo.
"""
from unittest.mock import patch, MagicMock
import pytest

from a_platform.b_contracts.z_interfaces.a_ide_adapter import IDEAdapter
from a_platform.b_contracts.j_state_manager import StateManager, ProjectPhase
from a_platform.b_contracts.i_execution_context import ExecutionContext


def test_resume_interface_continues_paused_project():
    """Valida o encaminhamento da resposta do usuário via IDEAdapter.continue_project."""
    adapter = IDEAdapter()
    project_id = "prj_resume_test"

    sm = StateManager(project_id=project_id)
    sm.current_phase = ProjectPhase.NEEDS_INPUT
    req = ExecutionContext(project_id=project_id)

    with patch.object(StateManager, "load_state", return_value=(sm, req)):
        with patch.object(adapter.orchestrator, "execute_pipeline", return_value="PAUSED"):
            adapter.orchestrator.state_manager = sm
            sm.project_ready = False
            sm.get_pending_question = MagicMock(return_value="Próxima pergunta")

            res = adapter.continue_project(project_id, answer="Minha resposta")
            assert res["project_id"] == project_id
            assert res["status"] in {"NEEDS_INPUT", "SUCCESS", "FAILED"}
