import pytest
from pydantic import ValidationError

from a_platform.a_core.b_domain.project import Project
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.project_plan import ProjectPlan
from a_platform.a_core.b_domain.discovery import DiscoveryResult
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.a_core.b_domain.execution import ExecutionResult
from a_platform.a_core.b_domain.certification import CertificationResult
from a_platform.a_core.c_orchestration.state_manager import StateManager

def test_project_instantiation():
    proj = Project(project_id="p1", name="Test", domain="finance")
    assert proj.project_id == "p1"
    assert proj.status == "REQUESTED"
    assert proj.metadata == {}

def test_project_request_validation():
    with pytest.raises(ValueError):
        ProjectRequest.from_raw("")
        
    req = ProjectRequest.from_raw("Create a dashboard", domain="sales")
    assert req.request == "Create a dashboard"
    assert req.domain == "sales"
    assert req.source == "cli"

def test_project_plan_instantiation():
    plan = ProjectPlan(project_id="p1", name="Plan A", domain="tech", phases=["phase1"])
    assert plan.phases == ["phase1"]

def test_discovery_result():
    discovery = DiscoveryResult(project_objective="Obj", confidence=0.9)
    assert discovery.confidence == 0.9

def test_artifact_serialization():
    art = Artifact(name="main.py", path="/src/main.py", content="print('hello')")
    data = art.model_dump()
    assert data["name"] == "main.py"
    assert "created_at" in data

def test_execution_result():
    ex = ExecutionResult(task_id="t1", success=True)
    assert ex.success is True
    assert ex.error is None

def test_certification_result():
    cert = CertificationResult(project_id="p1", passed=False, issues=["Bug 1"])
    assert cert.passed is False
    assert "Bug 1" in cert.issues

def test_state_manager():
    sm = StateManager()
    assert sm.get("status") == "INITIALIZED"
    
    sm.update("status", "STARTED")
    assert sm.get("status") == "STARTED"
    
    sm.update("status", "COMPLETED")
    assert sm.get("status") == "COMPLETED"
