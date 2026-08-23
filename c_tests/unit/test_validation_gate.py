import pytest
from unittest.mock import patch, MagicMock
from a_platform.j_validation.validation_gate import ValidationGate
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.project_plan import ProjectPlan

def test_validation_gate():
    gate = ValidationGate()
    request = ProjectRequest(project_id="test_proj", prompt="test")
    request.project_plan = ProjectPlan(project_id="test_proj", domain="generic")
    
    with patch("a_platform.j_validation.c_gates.pre_execution.PreExecutionGate.evaluate", return_value=True), \
         patch("a_platform.j_validation.c_gates.post_execution.PostExecutionGate.evaluate", return_value=True), \
         patch("a_platform.j_validation.c_gates.project_ready.ProjectReadyGate.evaluate", return_value=True):
        
        result = gate.run_validation(request)
        
    assert result is True

def test_validation_gate_fails():
    gate = ValidationGate()
    request = ProjectRequest(project_id="test_proj", prompt="test")
    request.project_plan = ProjectPlan(project_id="test_proj", domain="generic")
    
    with patch("a_platform.j_validation.c_gates.pre_execution.PreExecutionGate.evaluate", return_value=False):
        result = gate.run_validation(request)
        
    assert result is False
