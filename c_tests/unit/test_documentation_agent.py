import pytest
from unittest.mock import patch
from a_platform.c_agents.l_documentation.doc_agent import DocumentationAgent
from a_platform.a_core.b_domain.project_plan import ProjectPlan
from a_platform.a_core.b_domain.artifact import Artifact

@pytest.mark.asyncio
@patch("a_platform.c_agents.l_documentation.doc_agent.LLMGateway.generate")
async def test_documentation_agent_execution(mock_generate):
    mock_generate.return_value = "Mocked Response"
    agent = DocumentationAgent()
    plan = ProjectPlan(project_id="test-doc", name="Test Doc", domain="data", phases=[])
    artifacts = [Artifact(name="main.py", path="main.py", content="")]
    
    result = await agent.execute(plan, artifacts)
    
    assert result.name == "README.md"
    assert result.path == "README.md"
    assert "Analytics Project: test-doc" in result.content or "Test Doc" in result.content
