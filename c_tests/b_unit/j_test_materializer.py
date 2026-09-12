import os
import pytest
from unittest.mock import MagicMock, patch
from a_platform.h_factory.b_materializer.a_materializer import ArtifactMaterializer
from a_platform.a_core.a_contracts.e_execution_contract import Artifact
from a_platform.a_core.d_session.b_context import ExecutionContext
from a_platform.a_core.a_contracts.d_project_contract import ProjectPlan, Task

def test_materializer(tmp_path):
    mcp_mock = MagicMock()
    mcp_mock.execute_tool.return_value = {"success": True}
    
    materializer = ArtifactMaterializer(mcp=mcp_mock)
    
    request = ExecutionContext(project_id="test-proj", prompt="test")
    request.discovery_data = {"domain": "generic"}
    
    plan = ProjectPlan(project_id="test-proj", domain="generic")
    task = Task(id="1", name="test", description="test", agent="TestingAgent", expected_artifacts=["src/main.py", "requirements.txt"])
    plan.tasks = [task]
    request.project_plan = plan
    
    artifacts = [
        Artifact(name="src/main.py", content="print('hello')"),
        Artifact(name="requirements.txt", content="pytest")
    ]
    
    with patch("os.getcwd", return_value=str(tmp_path)), patch("os.path.exists", return_value=True):
        result = materializer.materialize(request, artifacts)
    
    assert result is True
    assert mcp_mock.execute_tool.call_count == 2
