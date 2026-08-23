import os
import pytest
from unittest.mock import MagicMock, patch
from a_platform.g_factory.d_artifact_materializer.materializer import ArtifactMaterializer
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.project_plan import ProjectPlan, Task

def test_materializer(tmp_path):
    mcp_mock = MagicMock()
    mcp_mock.execute_tool.return_value = {"success": True}
    
    materializer = ArtifactMaterializer(mcp=mcp_mock)
    
    request = ProjectRequest(project_id="test-proj", prompt="test")
    request.discovery_data = {"domain": "generic"}
    
    plan = ProjectPlan(project_id="test-proj", domain="generic")
    task = Task(id="1", name="test", description="test", agent="TestingAgent", expected_artifacts=["src/main.py", "requirements.txt"])
    plan.tasks = [task]
    request.project_plan = plan
    
    artifacts = [
        Artifact(name="src/main.py", path="src/main.py", content="print('hello')"),
        Artifact(name="requirements.txt", path="requirements.txt", content="pytest")
    ]
    
    with patch("os.getcwd", return_value=str(tmp_path)):
        result = materializer.materialize(request, artifacts)
    
    assert result is True
    assert mcp_mock.execute_tool.call_count == 2
