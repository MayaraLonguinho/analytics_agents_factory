import pytest
from unittest.mock import MagicMock
from a_platform.g_factory.a_project_factory.project_factory import ProjectFactory
from a_platform.a_core.b_domain.artifact import Artifact
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.project_plan import ProjectPlan, Task
from a_platform.c_agents.agent_factory import AgentFactory

def test_syntax_validation_blocks_invalid_python():
    agent_factory = AgentFactory()
    factory = ProjectFactory(agent_factory)
    
    request = ProjectRequest(prompt="", project_id="test", discovery_data={"domain": "analytics"})
    plan = ProjectPlan(project_id="test", domain="analytics")
    task = Task(id="t1", name="Task 1", description="", agent="data")
    plan.add_task(task)
    request.project_plan = plan
    
    # Mock do agent para retornar código python com SyntaxError (fechamento de parenteses sem abertura)
    mock_agent = MagicMock()
    mock_agent.execute_task.return_value = [
        Artifact(name="script.py", content="print('hello'))", type="code")
    ]
    
    agent_factory.get_agent = MagicMock(return_value=mock_agent)
    
    # A montagem deve lançar SyntaxError
    with pytest.raises(SyntaxError, match="Materialização abortada"):
        factory.assemble_project(request)

def test_syntax_validation_blocks_invalid_json():
    agent_factory = AgentFactory()
    factory = ProjectFactory(agent_factory)
    
    request = ProjectRequest(prompt="", project_id="test", discovery_data={"domain": "analytics"})
    plan = ProjectPlan(project_id="test", domain="analytics")
    task = Task(id="t1", name="Task 1", description="", agent="data")
    plan.add_task(task)
    request.project_plan = plan
    
    # Mock do agent para retornar JSON inválido
    mock_agent = MagicMock()
    mock_agent.execute_task.return_value = [
        Artifact(name="config.json", content="{ invalid json }", type="code")
    ]
    
    agent_factory.get_agent = MagicMock(return_value=mock_agent)
    
    with pytest.raises(SyntaxError, match="Materialização abortada"):
        factory.assemble_project(request)
