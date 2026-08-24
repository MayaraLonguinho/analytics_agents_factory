# pyrefly: ignore [missing-import]
import pytest
import os
from unittest.mock import MagicMock, patch, mock_open
from a_platform.k_quality.quality_engine import QualityEngine
from a_platform.a_core.b_domain.project_request import ProjectRequest

@pytest.fixture
def mock_quality_engine():
    engine = QualityEngine()
    # Mocking thresholds to be predictable
    engine.metrics = {
        "linting_weight": 0.2,
        "architecture_weight": 0.3,
        "documentation_weight": 0.2,
        "security_weight": 0.3
    }
    engine.passing_score = 60
    return engine

@patch("a_platform.k_quality.quality_engine.os.path.exists", return_value=True)
@patch("a_platform.k_quality.quality_engine.os.walk")
@patch("a_platform.k_quality.quality_engine.Linter")
@patch("a_platform.k_quality.quality_engine.SecurityScanner")
def test_quality_engine_security_failure(mock_sec_cls, mock_lint_cls, mock_walk, mock_exists, mock_quality_engine, tmp_path):
    # Setup mocks
    mock_walk.return_value = [("/mock/dir", [], ["main.py", "test_main.py"])]
    
    mock_lint = MagicMock()
    mock_lint.run_linter.return_value = {"passed": True}
    mock_lint_cls.return_value = mock_lint
    
    mock_sec = MagicMock()
    # SECURITY FAILURE
    mock_sec.run_scan.return_value = {"passed": False, "issues": "Critical eval() found"}
    mock_sec_cls.return_value = mock_sec
    
    request = ProjectRequest(project_id="test1", prompt="test")
    request.metadata = {}
    
    # Mock file open
    with patch("builtins.open", mock_open(read_data="def main(): pass")):
        result = mock_quality_engine.run_quality(request)
        
    assert result is False
    assert mock_sec.run_scan.called

@patch("a_platform.k_quality.quality_engine.os.path.exists", return_value=True)
@patch("a_platform.k_quality.quality_engine.os.walk")
@patch("a_platform.k_quality.quality_engine.Linter")
@patch("a_platform.k_quality.quality_engine.SecurityScanner")
def test_quality_engine_linter_penalty(mock_sec_cls, mock_lint_cls, mock_walk, mock_exists, mock_quality_engine, tmp_path):
    mock_walk.return_value = [("/mock/dir", [], ["main.py", "test_main.py"])]
    
    mock_lint = MagicMock()
    # LINTER FAILURE
    mock_lint.run_linter.return_value = {"passed": False}
    mock_lint_cls.return_value = mock_lint
    
    mock_sec = MagicMock()
    mock_sec.run_scan.return_value = {"passed": True}
    mock_sec_cls.return_value = mock_sec
    
    request = ProjectRequest(project_id="test1", prompt="test")
    request.metadata = {}
    
    with patch("builtins.open", mock_open(read_data="def main(): pass")):
        result = mock_quality_engine.run_quality(request)
        
    # The score should be penalized.
    # linting_score = 100 - 30 = 70
    # security_score = 100
    # architecture_score = 100
    # doc_score = 0 (no docstrings)
    # final_score = (70 * 0.2) + (100 * 0.3) + (0 * 0.2) + (100 * 0.3) = 14 + 30 + 0 + 30 = 74
    # 74 >= 60 (passing_score), so it should pass!
    assert result is True
    assert request.metadata["quality_score"] == 74
