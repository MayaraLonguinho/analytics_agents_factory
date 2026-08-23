# pyrefly: ignore [missing-import]
from unittest.mock import patch, MagicMock
from a_platform.j_validation.validation_gate import ValidationGate
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.project_plan import ProjectPlan
from a_platform.i_runtime.runtime_engine import RuntimeEngine
from a_platform.k_quality.quality_engine import QualityEngine


def test_validation_gate():
    gate = ValidationGate()
    request = ProjectRequest(project_id="test_proj", prompt="test")
    request.project_plan = ProjectPlan(
        project_id="test_proj", domain="generic"
    )
    request.metadata["runtime_payload"] = {"exit_code": 0}

    with patch(
        "a_platform.j_validation.c_gates.pre_execution.PreExecutionGate.evaluate",
        return_value=True
    ), patch(
        "a_platform.j_validation.c_gates.post_execution.PostExecutionGate.evaluate",
        return_value=True
    ), patch(
        "a_platform.j_validation.c_gates.project_ready.ProjectReadyGate.evaluate",
        return_value=True
    ):
        result = gate.run_validation(request)

    assert result is True


def test_validation_gate_fails():
    gate = ValidationGate()
    request = ProjectRequest(project_id="test_proj", prompt="test")
    request.project_plan = ProjectPlan(
        project_id="test_proj", domain="generic"
    )
    request.metadata["runtime_payload"] = {"exit_code": 0}

    with patch(
        "a_platform.j_validation.c_gates.pre_execution.PreExecutionGate.evaluate",
        return_value=False
    ):
        result = gate.run_validation(request)

    assert result is False


def test_execution_failure_blocks_validation_and_quality():
    request = ProjectRequest(project_id="test_proj", prompt="test")
    request.project_plan = ProjectPlan(
        project_id="test_proj", domain="generic", execution_required=True
    )
    request.metadata["runtime_payload"] = {"exit_code": 1}

    # 1. Validation deve falhar imediatamente
    val_gate = ValidationGate()
    assert val_gate.run_validation(request) is False

    # 2. Quality deve falhar imediatamente (consome falha de execução)
    qual_engine = QualityEngine()

    with patch("os.path.exists", return_value=True), \
         patch("os.walk", return_value=[("/f", [], ["main.py", "t.py"])]), \
         patch("builtins.open", return_value=MagicMock()), \
         patch("ast.parse", return_value=MagicMock()):

        assert qual_engine.run_quality(request) is False


def test_runtime_engine_empty_commands_fail():
    request = ProjectRequest(project_id="test_proj", prompt="test")
    request.project_plan = ProjectPlan(
        project_id="test_proj", domain="generic",
        execution_required=True, run_commands=[]
    )

    engine = RuntimeEngine()

    with patch("os.path.exists", return_value=True), \
         patch(
             "a_platform.i_runtime.runtime_engine.RuntimeEngine._run_subprocess",
             return_value=(True, "", "")
         ):

        result = engine.run_project(request)
        assert result is False
        msg = "Sem run_commands quando execution_required=True"
        assert msg in request.metadata.get("execution_error", "")


def test_runtime_engine_execution_not_required():
    request = ProjectRequest(project_id="test_proj", prompt="test")
    request.project_plan = ProjectPlan(
        project_id="test_proj", domain="generic",
        execution_required=False, run_commands=[]
    )

    engine = RuntimeEngine()

    with patch("os.path.exists", return_value=True):
        result = engine.run_project(request)
        assert result is True
        msg = "Execução desativada no plano (execution_required=False)"
        assert request.metadata["runtime_payload"]["stdout"] == msg
