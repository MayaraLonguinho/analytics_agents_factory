from unittest.mock import patch
from a_platform.j_quality.quality_engine import QualityEngine

@patch("a_platform.j_quality.security_scanner.subprocess.run")
@patch("a_platform.j_quality.linters.subprocess.run")
def test_quality_engine(mock_lint, mock_sec):
    mock_lint.return_value.returncode = 0
    mock_sec.return_value.returncode = 0
    
    engine = QualityEngine()
    result = engine.evaluate("/dummy/dir")
    
    assert result["passed"] is True
    assert result["lint_score"] == 100
    assert result["sec_score"] == 100
