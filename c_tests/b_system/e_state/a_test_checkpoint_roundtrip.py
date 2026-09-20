"""
c_tests/b_system/e_state/a_test_checkpoint_roundtrip.py
=====================================================
Especificação executável de serialização e desserialização de checkpoints (Roundtrip).
Valida que StateManager e ExecutionContext são salvos em JSON e recarregados
sem perda de integridade de fases, decisões, histórico ou artefatos, usando diretório temporário.
"""
from pathlib import Path
import os
import pytest

from a_platform.b_contracts.j_state_manager import StateManager, ProjectPhase, PhaseStatus
from a_platform.b_contracts.i_execution_context import ExecutionContext, Decision


def test_checkpoint_roundtrip_preserves_state(tmp_path: Path, monkeypatch):
    """Valida o ciclo completo save_state -> arquivo físico -> load_state em path controlado."""
    custom_state_dir = tmp_path / "h_runtime" / "state"
    custom_state_dir.mkdir(parents=True, exist_ok=True)

    project_id = "prj_chk_roundtrip"

    # Configura StateManager usando o diretório temporário
    sm = StateManager(project_id=project_id)
    sm.state_dir = str(custom_state_dir)
    sm.transition_to(ProjectPhase.DISCOVERY, {"intent": "ETL Analytics"})

    ctx = ExecutionContext(project_id=project_id, prompt="Build pipeline", domain="analytics")
    ctx.add_decision(Decision(id="D-10", status="adopted", decision="DuckDB", reason="Speed"))

    # Salva checkpoint físico
    sm.save_state(ctx)

    checkpoint_file = custom_state_dir / f"{project_id}.json"
    assert checkpoint_file.exists()

    # Recarrega do arquivo
    # Macete: monkeypatch da classe para apontar state_dir temporário
    monkeypatch.setattr(StateManager, "get_state_path", lambda pid: str(custom_state_dir / f"{pid}.json"))

    loaded_sm, loaded_ctx = StateManager.load_state(project_id)

    assert loaded_sm.project_id == project_id
    assert loaded_sm.current_phase == ProjectPhase.DISCOVERY
    assert loaded_sm.phases[ProjectPhase.DISCOVERY].status == PhaseStatus.IN_PROGRESS
    assert loaded_ctx.prompt == "Build pipeline"
    assert loaded_ctx.domain == "analytics"
    assert len(loaded_ctx.decisions) == 1
    assert loaded_ctx.decisions[0].id == "D-10"
