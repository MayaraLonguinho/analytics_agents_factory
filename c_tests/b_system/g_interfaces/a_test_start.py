"""
c_tests/b_system/g_interfaces/a_test_start.py
===========================================
Especificação executável da interface pública de inicialização de projetos (start).
Valida que o boundary de aplicação recebe prompt, dataset_path e project_id,
inicia o workflow da fábrica e retorna resultado estruturado.
"""
from unittest.mock import patch, MagicMock
import pytest

from a_platform.b_contracts.z_interfaces.a_ide_adapter import IDEAdapter


def test_start_interface_submits_new_project():
    """Valida a submissão de uma nova solicitação via IDEAdapter.create_project."""
    adapter = IDEAdapter()

    with patch.object(adapter.orchestrator, "execute_pipeline", return_value="PAUSED") as mock_exec:
        adapter.orchestrator.state_manager = MagicMock()
        adapter.orchestrator.state_manager.current_phase.name = "NEEDS_INPUT"
        adapter.orchestrator.state_manager.project_ready = False
        adapter.orchestrator.state_manager.get_pending_question.return_value = "Qual a fonte?"

        res = adapter.create_project(
            prompt="Construir pipeline analítico",
            dataset_path="b_input/a_vendas.csv",
            project_id="prj_start_test",
        )

        assert res["project_id"] == "prj_start_test"
        assert res["status"] == "NEEDS_INPUT"
        assert "Qual a fonte?" in res["question"]
