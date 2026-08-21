import pytest
from unittest.mock import patch, MagicMock
from a_platform.a_core.c_orchestration.orchestrator import MasterOrchestrator

def make_mock_run(val_code=0, lint_code=0, sec_code=0):
    def side_effect(args, **kwargs):
        mock = MagicMock()
        if args and args[0] == "pytest":
            mock.returncode = val_code
        elif args and args[0] == "flake8":
            mock.returncode = lint_code
        elif args and args[0] == "bandit":
            mock.returncode = sec_code
        else:
            mock.returncode = 0
        return mock
    return side_effect

@pytest.mark.asyncio
@patch("a_platform.h_runtime.docker_controller.subprocess.run")
@patch("a_platform.h_runtime.health_checker.urllib.request.urlopen")
@patch("subprocess.run")
async def test_run_pipeline_success(mock_sub_run, mock_url, mock_docker_run, tmp_path):
    # Setup mocks for runtime
    mock_docker_run.return_value.returncode = 0
    class MockResponse:
        def getcode(self): return 200
    mock_url.return_value = MockResponse()
    
    # Setup mock for certification (test_runner, linters, scanner)
    mock_sub_run.side_effect = make_mock_run(val_code=0, lint_code=0, sec_code=0)
    
    orchestrator = MasterOrchestrator()
    # Change materializer base dir to avoid polluting actual project
    orchestrator.materializer.base_dir = str(tmp_path / "e_generated_projects")
    
    state = await orchestrator.run_pipeline("Create a generic analytics platform")
    
    assert state.get("status") == "COMPLETED_SUCCESS"
    
    cert = state.get("certification")
    assert cert.is_certified is True
    assert cert.tier == "PLATINUM"
    assert cert.metrics["final_score"] == 100.0
    
    artifacts = state.get("artifacts")
    assert len(artifacts) == 6
