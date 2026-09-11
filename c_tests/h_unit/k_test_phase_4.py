# pyrefly: ignore [missing-import]
import pytest
import ast
from unittest.mock import MagicMock, patch
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.l_quality.quality_engine import QualityEngine
from a_platform.m_certification.certification_engine import CertificationEngine
from a_platform.a_core.c_orchestration.state_manager import StateManager, ProjectPhase, PhaseStatus
from a_platform.a_core.b_domain.readiness import ReadinessGate
from a_platform.n_learning.repair.repair_loop import RepairLoop

def test_quality_and_certification():
    request = ProjectRequest(project_id="test_proj", prompt="test")
    request.discovery_data = {"domain": "generic"}
    
    # Mock Quality Engine
    quality = QualityEngine()
    
    # Create fake valid ast module
    fake_tree = ast.parse("def fake():\n  '''doc'''\n  pass")
    
    with patch("os.path.exists", return_value=True):
        with patch("os.walk", return_value=[("/fake/path", [], ["main.py", "test_main.py"])]):
            with patch("builtins.open", return_value=MagicMock()):
                with patch("ast.parse", return_value=fake_tree):
                    # Should pass
                    res = quality.run_quality(request)
                    assert res is True
                    assert request.metadata["quality_score"] > 60

    # Certificaton Engine
    cert = CertificationEngine()
    state_manager = StateManager(project_id="test_proj")
    
    # Simulate success on all gates
    state_manager.phases[ProjectPhase.DISCOVERY].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.PLANNER].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.MATERIALIZATION].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.EXECUTION].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.VALIDATION].status = PhaseStatus.COMPLETED
    state_manager.phases[ProjectPhase.QUALITY].status = PhaseStatus.COMPLETED
    
    with patch("os.makedirs", return_value=True):
        with patch("builtins.open", return_value=MagicMock()):
            res = cert.run_certification(request, state_manager)
            assert res is True
            assert request.metadata["certification_tier"] in ["SILVER", "GOLD", "PLATINUM"]
            
    # Readiness Gate
    state_manager.phases[ProjectPhase.CERTIFICATION].status = PhaseStatus.COMPLETED
    assert ReadinessGate.evaluate(state_manager) is True

    # Test Execution Failure blocks Certification and Readiness
    state_manager.phases[ProjectPhase.EXECUTION].status = PhaseStatus.FAILED
    with patch("os.makedirs", return_value=True):
        with patch("builtins.open", return_value=MagicMock()):
            res_fail = cert.run_certification(request, state_manager)
            assert res_fail is False
    
    state_manager.phases[ProjectPhase.CERTIFICATION].status = PhaseStatus.FAILED
    assert ReadinessGate.evaluate(state_manager) is False

def test_repair_loop_max_attempts():
    repair = RepairLoop(agent_factory=MagicMock(), learning_engine=MagicMock())
    repair.gateway.generate = MagicMock(return_value={"success": True, "text": '{"file_name": "test.py", "agent_type": "backend", "fixed_content": "print()"}', "provider": "mock"})
    repair.mcp.execute_tool = MagicMock(return_value={"success": True})
    
    request = ProjectRequest(project_id="test_proj", prompt="test")
    request.discovery_data = {"domain": "generic"}
    request.metadata["execution_error"] = "SyntaxError"
    
    # 0 -> 1
    repair.run_repair(request)
    assert request.metadata.get("repair_attempts", 1) == 1
    
    request.metadata["execution_error"] = "SyntaxError"
    # 1 -> 2
    repair.run_repair(request)
    assert request.metadata.get("repair_attempts", 2) == 2
    
    request.metadata["execution_error"] = "SyntaxError"
    # 2 -> 3
    repair.run_repair(request)
    assert request.metadata.get("repair_attempts", 3) == 3
    
    request.metadata["execution_error"] = "SyntaxError"
    # 3 -> Limit Exceeded
    res = repair.run_repair(request)
    assert res is False
