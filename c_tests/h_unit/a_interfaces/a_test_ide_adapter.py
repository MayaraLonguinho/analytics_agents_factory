# pyrefly: ignore [missing-import]
import pytest
import sys
from unittest.mock import patch, MagicMock

# Mock components that need to hit the LLM or DB
sys.modules['a_platform.g_llm_gateway.gateway'] = MagicMock()
sys.modules['a_platform.d_agents.agent_factory'] = MagicMock()
sys.modules['a_platform.h_factory.a_project_factory.project_factory'] = MagicMock()

from a_platform.b_interfaces.a_ide.adapter import IDEAdapter

@patch('a_platform.b_interfaces.a_ide.adapter.MasterOrchestrator')
def test_create_project_invalid_prompt(mock_orchestrator):
    adapter = IDEAdapter()
    
    # Empty prompt
    resp1 = adapter.create_project(prompt="")
    assert resp1.success is False
    assert "não pode estar vazio" in resp1.error
    
    # Whitespace prompt
    resp2 = adapter.create_project(prompt="   ")
    assert resp2.success is False
    assert "não pode estar vazio" in resp2.error
    
    # Mock SHOULD NOT be called if validation fails
    mock_orchestrator.assert_not_called()

@patch('a_platform.b_interfaces.a_ide.adapter.MasterOrchestrator')
def test_create_project_valid_prompt(mock_orchestrator):
    adapter = IDEAdapter()
    
    # Setup mock to return success
    instance = mock_orchestrator.return_value
    instance.execute_pipeline.return_value = "SUCCESS"
    
    resp = adapter.create_project(prompt="Crie um pipeline de dados")
    assert resp.success is True
    assert resp.status == "READY"
    
    # Ensure orchestrator was instantiated and pipeline was executed
    mock_orchestrator.assert_called_once()
    instance.execute_pipeline.assert_called_once()

def test_continue_project_invalid_input():
    adapter = IDEAdapter()
    
    # Invalid project id
    resp1 = adapter.continue_project(project_id="", user_response="Sim, prossiga.")
    assert resp1.success is False
    assert "project_id não pode estar vazio" in resp1.error
    
    # Invalid user response
    resp2 = adapter.continue_project(project_id="proj_123", user_response="  ")
    assert resp2.success is False
    assert "resposta do usuário não pode estar vazia" in resp2.error
