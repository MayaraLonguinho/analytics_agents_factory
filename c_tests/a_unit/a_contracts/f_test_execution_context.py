"""
c_tests/a_unit/a_contracts/f_test_execution_context.py
====================================================
Especificação executável do contrato ExecutionContext, Decision, Gates e SkillRecord.
Valida o acúmulo de decisões arquiteturais, tracking de skills e status dos gates.
"""
import pytest

from a_platform.b_contracts.i_execution_context import (
    ExecutionContext,
    Decision,
    Gates,
    SkillRecord,
)


def test_execution_context_initialization():
    """Valida a inicialização padrão de ExecutionContext."""
    ctx = ExecutionContext(project_id="prj_ctx_1", prompt="Build ETL")
    assert ctx.project_id == "prj_ctx_1"
    assert ctx.prompt == "Build ETL"
    assert ctx.dataset_path is None
    assert isinstance(ctx.gates, Gates)
    assert ctx.decisions == []
    assert ctx.skills == []


def test_add_decision_and_freeze():
    """Valida o registro de decisões de arquitetura e o congelamento do contexto."""
    ctx = ExecutionContext(project_id="prj_ctx_2")
    decision = Decision(
        id="D-001",
        status="adopted",
        decision="Use DuckDB for embedded analytical queries",
        reason="Zero setup, high performance OLAP",
    )
    ctx.add_decision(decision)
    assert len(ctx.decisions) == 1
    assert ctx.decisions[0].id == "D-001"
    assert ctx.decisions[0].status == "adopted"

    # Congela o contexto e valida imutabilidade de metadados
    ctx.freeze_context()
    assert ctx.metadata.get("frozen") is True


def test_gates_progression_tracking():
    """Valida os estados dos gates no ExecutionContext."""
    ctx = ExecutionContext(project_id="prj_ctx_3")
    assert ctx.gates.discovery == "pending"
    assert ctx.gates.validation == "pending"

    ctx.gates.discovery = "passed"
    ctx.gates.validation = "passed"
    assert ctx.gates.discovery == "passed"
    assert ctx.gates.validation == "passed"
