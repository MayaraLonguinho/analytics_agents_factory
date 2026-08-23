from unittest.mock import patch, MagicMock
from a_platform.l_certification.certification_engine import CertificationEngine

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

@patch("subprocess.run")
def test_certification_engine_platinum(mock_run):
    mock_run.side_effect = make_mock_run(val_code=0, lint_code=0, sec_code=0)
    
    engine = CertificationEngine()
    result = engine.certify_project("proj-123", "/dummy/dir")
    
    assert result.tier == "PLATINUM"
    assert result.is_certified is True
    assert result.metrics["final_score"] == 100.0

@patch("subprocess.run")
def test_certification_engine_silver(mock_run):
    mock_run.side_effect = make_mock_run(val_code=0, lint_code=1, sec_code=1)
    
    engine = CertificationEngine()
    result = engine.certify_project("proj-123", "/dummy/dir")
    
    assert result.tier == "SILVER"
    assert result.is_certified is True
    assert result.metrics["final_score"] == 77.5

@patch("subprocess.run")
def test_certification_engine_rejected(mock_run):
    mock_run.side_effect = make_mock_run(val_code=1, lint_code=1, sec_code=1)
    
    engine = CertificationEngine()
    result = engine.certify_project("proj-123", "/dummy/dir")
    
    assert result.tier == "REJECTED"
    assert result.is_certified is False
    assert result.metrics["final_score"] == 37.5
