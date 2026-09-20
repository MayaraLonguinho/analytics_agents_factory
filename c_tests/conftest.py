"""
c_tests/conftest.py
===================
Fixtures compartilhadas para a suíte de testes da Analytics Agents Factory (AAF).
Fornece recursos controlados e determinísticos sem mascarar testes de configuração
através de variáveis de ambiente globais indiscriminadas.
"""
from pathlib import Path
from typing import Dict, Any
import pytest

from a_platform.b_contracts.a_project import ProjectContext
from a_platform.b_contracts.e_task import ProjectTask
from a_platform.b_contracts.f_plan import ProjectPlan
from a_platform.b_contracts.g_artifact import Artifact
from a_platform.b_contracts.i_execution_context import ExecutionContext, Decision
from a_platform.j_llm_gateway.a_interfaces.a_base_provider import LLMResponse


@pytest.fixture
def sample_project_id() -> str:
    """Retorna um identificador de projeto único e previsível para testes."""
    return "prj_test_1001"


@pytest.fixture
def temp_project_dir(tmp_path: Path) -> Path:
    """Diretório temporário isolado para emulação de materialização e sandbox de execução."""
    project_dir = tmp_path / "e_generated_projects" / "prj_test_1001"
    project_dir.mkdir(parents=True, exist_ok=True)
    return project_dir


@pytest.fixture
def sample_task() -> ProjectTask:
    """Retorna uma Task canônica do AAF com capacidades e artefatos esperados."""
    return ProjectTask(
        task_id="t1_ingest",
        name="Ingest Sales Data",
        assigned_agent="DataAgent",
        required_skills=["data-ingestion"],
        dependencies=[],
        expected_artifacts=["ingestion.py"],
        commands=["python main.py"],
        validators=["test_syntax"],
    )


@pytest.fixture
def sample_plan(sample_task: ProjectTask, sample_project_id: str) -> ProjectPlan:
    """Retorna um ProjectPlan canônico do AAF contendo uma task estruturada."""
    return ProjectPlan(
        project_id=sample_project_id,
        tasks=[sample_task],
    )


@pytest.fixture
def sample_artifact() -> Artifact:
    """Retorna um Artifact representativo produzido por uma Skill da fábrica."""
    return Artifact(
        identity="art_1_ingest",
        name="ingest.py",
        path="src/ingest.py",
        type="code",
        content="def ingest(): return 'ok'",
        producer="data-ingestion",
    )


@pytest.fixture
def sample_execution_context(sample_project_id: str) -> ExecutionContext:
    """Retorna um ExecutionContext limpo e tipado para execução de testes."""
    ctx = ExecutionContext(
        project_id=sample_project_id,
        prompt="Criar pipeline de dados para análise de vendas",
        dataset_path="b_input/a_vendas.csv",
        domain="analytics",
    )
    ctx.add_decision(
        Decision(
            id="D-001",
            status="adopted",
            decision="Utilizar SQLite para banco local",
            reason="Simplicidade operacional e zero dependência externa",
        )
    )
    return ctx


@pytest.fixture
def mock_api_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Fixture explícita (não autouse) para testes que exigem credenciais mockadas de LLM.
    Deve ser solicitada deliberadamente para não mascarar testes de configuração.
    """
    monkeypatch.setenv("OPENAI_API_KEY", "sk-mock-openai-key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-mock-anthropic-key")
    monkeypatch.setenv("GEMINI_API_KEY", "sk-mock-gemini-key")


@pytest.fixture
def mock_llm_response_factory():
    """Factory de respostas LLM estruturadas para testes com provedor determinístico."""
    def _create(content: str, model: str = "gpt-4o-mini", provider: str = "openai") -> LLMResponse:
        return LLMResponse(
            content=content,
            model=model,
            provider=provider,
            metadata={"finish_reason": "stop"},
        )
    return _create
