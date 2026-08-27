# pyrefly: ignore [missing-import]
import pytest
from unittest.mock import patch
from a_platform.d_agents.specialized_agents import (
    DataAgent, DatabaseAgent, AnalyticsAgent, TestingAgent, InfrastructureAgent
)
TestingAgent.__test__ = False
from a_platform.a_core.b_domain.project_plan import Task
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.artifact import Artifact

@pytest.fixture
def mock_request():
    return ProjectRequest(prompt="Test specialized agent", project_id="test_id")

@patch('a_platform.d_agents.base_agent.BaseAgent.execute_task')
def test_data_agent_injects_rules(mock_super, mock_request):
    agent = DataAgent(name="Data", gateway=None, mcp=None, skills=None)
    task = Task(id="1", name="Test Data", description="Do ETL", skills=["some_skill", "dataset_profiling"], agent="DataAgent")
    
    mock_super.return_value = [Artifact(name="etl.py", content="print('hello')", type="source_code")]
    agent.execute_task(task, mock_request)
    
    assert mock_super.called
    called_task = mock_super.call_args[0][0]
    assert "REGRAS DE DADOS/ETL:" in called_task.description
    assert "dataset_profiling" in called_task.skills

@patch('a_platform.d_agents.base_agent.BaseAgent.execute_task')
def test_database_agent_injects_rules(mock_super, mock_request):
    agent = DatabaseAgent(name="Database", gateway=None, mcp=None, skills=None)
    task = Task(id="1", name="Test DB", description="Create schema", skills=[], agent="DatabaseAgent")
    
    mock_super.return_value = [Artifact(name="schema.sql", content="CREATE TABLE a (id int);", type="source_code")]
    agent.execute_task(task, mock_request)
    
    assert mock_super.called
    called_task = mock_super.call_args[0][0]
    assert "REGRAS DE BANCO DE DADOS:" in called_task.description
    assert "sql_generation" in called_task.skills

@patch('a_platform.d_agents.base_agent.BaseAgent.execute_task')
def test_analytics_agent_injects_rules(mock_super, mock_request):
    agent = AnalyticsAgent(name="Analytics", gateway=None, mcp=None, skills=None)
    task = Task(id="1", name="Test Analytics", description="Write query", skills=[], agent="AnalyticsAgent")
    
    mock_super.return_value = [Artifact(name="queries.sql", content="SELECT * FROM a;", type="source_code")]
    agent.execute_task(task, mock_request)
    
    assert mock_super.called
    called_task = mock_super.call_args[0][0]
    assert "REGRAS ANALÍTICAS:" in called_task.description
    assert "sql_generation" in called_task.skills

@patch('a_platform.d_agents.base_agent.BaseAgent.execute_task')
def test_testing_agent_injects_rules(mock_super, mock_request):
    agent = TestingAgent(name="Testing", gateway=None, mcp=None, skills=None)
    task = Task(id="1", name="Test QA", description="Write tests", skills=[], agent="TestingAgent")
    
    mock_super.return_value = [Artifact(name="test_etl.py", content="def test_a(): pass", type="source_code")]
    agent.execute_task(task, mock_request)
    
    assert mock_super.called
    called_task = mock_super.call_args[0][0]
    assert "REGRAS DE TESTING:" in called_task.description

@patch('a_platform.d_agents.base_agent.BaseAgent.execute_task')
def test_infrastructure_agent_injects_rules(mock_super, mock_request):
    agent = InfrastructureAgent(name="Infrastructure", gateway=None, mcp=None, skills=None)
    task = Task(id="1", name="Test Infra", description="Write Dockerfile", skills=[], agent="InfrastructureAgent")
    
    mock_super.return_value = [Artifact(name="Dockerfile", content="FROM python:3", type="source_code")]
    agent.execute_task(task, mock_request)
    
    assert mock_super.called
    called_task = mock_super.call_args[0][0]
    assert "REGRAS DE INFRA:" in called_task.description
