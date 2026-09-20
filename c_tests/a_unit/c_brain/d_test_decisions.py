"""
c_tests/a_unit/c_brain/d_test_decisions.py
========================================
Especificação executável do registro e governança de decisões arquiteturais.
Valida o ciclo de vida das decisões (D-NNN) adotadas no contexto analítico.
"""
import pytest

from a_platform.b_contracts.i_execution_context import Decision, ExecutionContext


def test_decision_lifecycle_recording():
    """Valida o registro de decisão de arquitetura técnica com justificativa e evidência."""
    ctx = ExecutionContext(project_id="prj_dec_1")
    dec = Decision(
        id="D-001",
        status="adopted",
        decision="Utilizar SQLite local para persistência dos dados transformados",
        reason="Ambiente autocontido e facilidade de execução local sem dependências externas",
        evidence="Dataset com 10.000 linhas cabe perfeitamente em banco local",
    )
    ctx.add_decision(dec)
    assert len(ctx.decisions) == 1
    stored = ctx.decisions[0]
    assert stored.id == "D-001"
    assert stored.status == "adopted"
    assert "SQLite" in stored.decision
    assert stored.evidence != ""


def test_multiple_decisions_ordering():
    """Valida a preservação da ordem e rastreabilidade de múltiplas decisões."""
    ctx = ExecutionContext(project_id="prj_dec_2")
    d1 = Decision(id="D-001", status="adopted", decision="Pandas", reason="ETL")
    d2 = Decision(id="D-002", status="adopted", decision="Pytest", reason="Testing")
    ctx.add_decision(d1)
    ctx.add_decision(d2)
    assert len(ctx.decisions) == 2
    assert ctx.decisions[0].id == "D-001"
    assert ctx.decisions[1].id == "D-002"
