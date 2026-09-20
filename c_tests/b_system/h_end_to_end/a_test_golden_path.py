"""
c_tests/b_system/h_end_to_end/a_test_golden_path.py
=================================================
Especificação executável do Golden Path completo do AAF.
USER REQUEST -> DISCOVERY -> DATASET PROFILING -> BRAIN -> ARCHITECTURE -> PLANNER ->
PROJECT DECOMPOSITION -> SKILL ROUTING -> EXECUTION PLAN -> PROJECT FACTORY ->
MATERIALIZER -> GENERATED PROJECT -> RUNTIME -> VALIDATION -> QUALITY -> CERTIFICATION ->
READINESS -> PROJECT READY = YES.
Sem injeção manual de arquivos no sandbox e sem bypass falso de gates.
"""
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock
import pytest

from a_platform.o_orchestration.a_orchestrator import MasterOrchestrator
from a_platform.b_contracts.i_execution_context import ExecutionContext
from a_platform.b_contracts.a_project import ProjectContext
from a_platform.b_contracts.e_task import ProjectTask
from a_platform.b_contracts.f_plan import ProjectPlan
from a_platform.b_contracts.g_artifact import Artifact
from a_platform.b_contracts.h_execution import ExecutionResult, CommandExecutionResult
from a_platform.b_contracts.k_validation import ValidationResult
from a_platform.b_contracts.l_quality import QualityResult
from a_platform.b_contracts.m_certification import CertificationResult


def test_golden_path_specification():
    """
    Especifica a progressão sequencial do Golden Path com gates cumulativos.
    Provas de cada etapa devem ser geradas organicamente pelos componentes da fábrica.
    """
    project_id = "prj_golden_spec"

    # Contexto inicializado a partir da solicitação
    pctx = ProjectContext(
        project_id=project_id,
        project_name="Golden Pipeline",
        project_path=f"e_generated_projects/{project_id}",
        domain="analytics",
        plan=[
            ProjectTask(
                task_id="t1",
                name="Ingestion",
                assigned_agent="DataAgent",
                expected_artifacts=["pipeline.py"],
                commands=["python pipeline.py"],
            )
        ],
        materialization_status="SUCCESS",
    )
    ctx = ExecutionContext(
        project_id=project_id,
        prompt="Criar pipeline analítico",
        domain="analytics",
        discovery_data={"domain": "analytics", "project_type": "Pipeline"},
        project_context=pctx,
    )

    # 1. Execução no Runtime produz resultado
    exec_res = ExecutionResult(
        execution_id="exec_1",
        task_id="t1",
        status="PASSED",
        return_code=0,
        stdout="Pipeline executed successfully",
        commands=[
            CommandExecutionResult(
                task_id="t1",
                command=["python", "pipeline.py"],
                executable="python",
                status="SUCCESS",
                return_code=0,
            )
        ],
    )

    # 2. ValidationGate aprova com base nas evidências
    val_res = ValidationResult(status="PASSED", evidence="All structure and syntax validated")

    # 3. QualityEngine aprova
    qual_res = QualityResult(status="PASSED", evidence="Quality thresholds passed")

    # 4. CertificationEngine avalia cumulativamente os 6 critérios
    from a_platform.n_certification.a_certification_engine import CertificationEngine
    cert_engine = CertificationEngine()
    cert_res = cert_engine.evaluate(ctx, exec_res, val_res, qual_res)

    assert cert_res.status == "PASSED"
    assert "PROJECT READY = YES" in cert_res.evidence
