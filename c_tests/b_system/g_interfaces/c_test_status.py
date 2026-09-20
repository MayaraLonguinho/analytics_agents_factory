"""
c_tests/b_system/g_interfaces/c_test_status.py
============================================
Especificação executável da interface pública de consulta de status (status).
Valida que o estado operacional da máquina de estados pode ser consultado
e formatado de forma limpa para apresentação na CLI ou IDE.
"""
import pytest

from a_platform.b_contracts.j_state_manager import StateManager, ProjectPhase


def test_status_interface_returns_phase_details():
    """Valida a consulta do status de fases via StateManager.get_status()."""
    project_id = "prj_status_test"
    sm = StateManager(project_id=project_id)
    sm.transition_to(ProjectPhase.DISCOVERY, {"goal": "ETL"})

    status_data = sm.get_status()
    assert "project_id" in status_data
    assert status_data["project_id"] == project_id
    assert status_data["current_phase"] == "DISCOVERY"
    assert "phases" in status_data
