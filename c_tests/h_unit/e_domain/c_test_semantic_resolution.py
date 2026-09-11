# pyrefly: ignore [missing-import]
import pytest
import sys
from unittest.mock import patch, MagicMock
import a_platform.a_core.c_orchestration.state_manager as sm

# Mocking LLMGateway entirely to avoid LLM imports
sys.modules['a_platform.g_llm_gateway.gateway'] = MagicMock()
sys.modules['a_platform.d_agents.agent_factory'] = MagicMock()
sys.modules['a_platform.h_factory.a_project_factory.project_factory'] = MagicMock()

from a_platform.a_core.c_orchestration.orchestrator import MasterOrchestrator
from a_platform.a_core.b_domain.project_request import ExecutionContext
from a_platform.d_agents.b_discovery.discovery_agent import DiscoveryStatus

class MockDiscoveryAgent:
    def __init__(self, mock_data):
        self.mock_data = mock_data
    def run_discovery(self, request):
        request.discovery_data.update(self.mock_data)
        return DiscoveryStatus.COMPLETE

def test_orchestrator_semantic_resolution_sales():
    orchestrator = MasterOrchestrator()
    request = ExecutionContext(prompt="test", project_id="test_id")
    
    orchestrator.discovery_agent = MockDiscoveryAgent({
        "project_type": "ETL",
        "business_context": "sales",
        "domain": "data_engineering"
    })
    
    orchestrator.state_manager = sm.StateManager("test_id")
    
    success = orchestrator._step_discovery(request)
    assert success is True
    
    assert request.business_context == "sales"
    assert request.domain == "data_engineering"
    assert request.discovery_data["domain"] == "data_engineering"

def test_orchestrator_semantic_resolution_finance():
    orchestrator = MasterOrchestrator()
    request = ExecutionContext(prompt="test", project_id="test_id")
    
    orchestrator.discovery_agent = MockDiscoveryAgent({
        "project_type": "Dashboard Analítico",
        "business_context": "finance",
        "domain": "analytics"
    })
    
    orchestrator.state_manager = sm.StateManager("test_id")
    
    success = orchestrator._step_discovery(request)
    assert success is True
    
    assert request.business_context == "finance"
    assert request.domain == "analytics"
    assert request.discovery_data["domain"] == "analytics"

def test_orchestrator_semantic_resolution_inventory():
    orchestrator = MasterOrchestrator()
    request = ExecutionContext(prompt="test", project_id="test_id")
    
    orchestrator.discovery_agent = MockDiscoveryAgent({
        "project_type": "Data Pipeline",
        "business_context": "inventory",
        "domain": "data_engineering"
    })
    
    orchestrator.state_manager = sm.StateManager("test_id")
    
    success = orchestrator._step_discovery(request)
    assert success is True
    
    assert request.business_context == "inventory"
    assert request.domain == "data_engineering"
    assert request.discovery_data["domain"] == "data_engineering"

def test_orchestrator_unknown_domain():
    orchestrator = MasterOrchestrator()
    request = ExecutionContext(prompt="test", project_id="test_id")
    
    orchestrator.discovery_agent = MockDiscoveryAgent({
        "project_type": "Sistema X",
        "business_context": "financeiro",
        "domain": "financeiro" # Invalid domain should cause an exception
    })
    
    orchestrator.state_manager = sm.StateManager("test_id")
    
    with pytest.raises(ValueError) as exc:
        orchestrator._step_discovery(request)
        
    assert "Domínio técnico inválido ou ausente" in str(exc.value) or "Domínio técnico não pode ser vazio" in str(exc.value)
