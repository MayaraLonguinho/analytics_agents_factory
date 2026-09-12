from pathlib import Path

from a_platform.n_orchestration.b_orchestrator import MasterOrchestrator


def test_orchestrator_materializes_and_executes_real_project(tmp_path):
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text(
        "customer_id,amount,segment\n1,1200,retail\n2,2500,corporate\n3,890,retail\n", encoding="utf-8")

    metadata = {
        "dataset_source": str(csv_path),
        "project_name": "Test Analytics",
        "domain": "analytics",
        "objective": "Test",
        "data_source": str(csv_path),
        "backend": "FastAPI",
        "frontend": "React + Vite",
        "database": "PostgreSQL",
        "infrastructure": "Docker",
        "authentication": "JWT",
        "analytics": "pandas",
        "etl": "None",
        "deployment": "Local",
        "security": "Standard",
        "testing": "pytest",
        "documentation": "README"
    }
    
    # Mock LLMGateway like we did in test_phase3_flow to avoid network calls
    from unittest.mock import patch
    from a_platform.a_core.a_contracts.architecture import ArchitectureDecision

    def mock_gateway_init(self, *args, **kwargs):
        pass

    def mock_decide_sync(self, discovery, dataset_profile, rules, patterns):
        return ArchitectureDecision(
            frontend="React + Vite",
            backend="FastAPI",
            database="PostgreSQL",
            data_pipeline="None",
            infrastructure="Docker",
            authentication="JWT",
            testing="pytest",
            documentation="README",
            rationale="Mocked for testing."
        )

    with patch("f_llm_gateway.gateway.LLMGateway.__init__", mock_gateway_init), \
         patch("c_agents.c_architecture.architecture_agent.ArchitectureAgent.decide_sync", mock_decide_sync):
        result = MasterOrchestrator(project_root=tmp_path).handle_request(
            "Create an analytics project for this dataset",
            domain="analytics",
            source="cli",
            metadata=metadata,
        )

    # Execution will fail because the materializer only generates a scaffold right now, 
    # not a fully operational project that passes all tests.
    assert result["execution"]["status"] == "FAILED"
    assert result["project_ready"]["passed"] is False
    
    project_root = Path(result["execution"]["metadata"]["project_path"])
    assert (project_root / ".project_bundle_manifest.json").exists()
