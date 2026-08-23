from unittest.mock import patch
from a_platform.j_validation.validation_gate import ValidationGate

@patch("a_platform.j_validation.test_runner.subprocess.run")
def test_validation_gate(mock_run):
    mock_run.return_value.returncode = 0
    mock_run.return_value.stdout = "tests passed"
    mock_run.return_value.stderr = ""
    
    gate = ValidationGate()
    result = gate.validate("/dummy/dir")
    
    assert result["is_valid"] is True
    assert result["details"]["output"] == "tests passed"
