import pytest
from unittest.mock import patch, MagicMock
from a_platform.j_validation.validation_gate import ValidationGate
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.project_plan import ProjectPlan

@patch("a_platform.j_validation.validation_gate.subprocess.run")
def test_validation_gate(mock_run):
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = "tests passed"
    mock_run.return_value.stderr = ""
    
    gate = ValidationGate()
    request = ProjectRequest(project_id="test_proj", prompt="test")
    request.project_plan = ProjectPlan(project_id="test_proj", domain="generic")
    
    # Needs some mock to not fail on os.path.exists
    with patch("os.path.exists", return_value=True):
        result = gate.run_validation(request)
    
    assert result is True
