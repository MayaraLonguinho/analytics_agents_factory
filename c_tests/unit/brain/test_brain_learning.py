# pyrefly: ignore [missing-import]
import pytest
import os
import yaml
from unittest.mock import MagicMock, patch, mock_open
from a_platform.m_learning.brain_updater import BrainUpdater, KnowledgeItem
from a_platform.b_brain.f_registry.knowledge_registry import KnowledgeRegistry
from a_platform.c_agents.c_architecture.architecture_agent import ArchitectureAgent
from a_platform.a_core.b_domain.project_request import ProjectRequest

def test_brain_updater_saves_lesson(tmp_path):
    updater = BrainUpdater()
    updater.domains_path = str(tmp_path)
    
    item = KnowledgeItem(domain="analytics", pattern="SyntaxError in Pandas", recommendation="Use pandas correctly")
    updater.save_lesson(item)
    
    expected_path = os.path.join(updater.domains_path, "analytics", "learned_rules.yaml")
    assert os.path.exists(expected_path)
    
    with open(expected_path, "r") as f:
        data = yaml.safe_load(f)
        
    assert "rules" in data
    assert len(data["rules"]) == 1
    assert data["rules"][0]["pattern"] == "SyntaxError in Pandas"

@patch("a_platform.b_brain.f_registry.knowledge_registry.KnowledgeRegistry")
@patch("a_platform.c_agents.c_architecture.architecture_agent.LLMGateway")
def test_architecture_agent_uses_learned_rules(mock_gateway_cls, mock_registry_cls):
    mock_gateway = MagicMock()
    # Mock LLM generation
    mock_gateway.generate.return_value = {
        "success": True, 
        "text": '{"core_stack": "python", "database_technology": "pg", "architecture_pattern": "mvc", "data_processing": "pandas", "rationale": "test"}'
    }
    mock_gateway_cls.return_value = mock_gateway
    
    mock_registry = MagicMock()
    mock_registry.get_learned_rules_for_domain.return_value = [
        {"domain": "analytics", "pattern": "Bad architecture", "recommendation": "Use good architecture"}
    ]
    mock_registry_cls.return_value = mock_registry
    
    # Mock Brain
    mock_brain = MagicMock()
    mock_brain.get_project_context.return_value = {}
    mock_brain.retrieve_relevant_knowledge.return_value = {}
    
    mock_graph_builder = MagicMock()
    mock_graph_builder.build_graph.return_value = {"nodes": []}
    
    agent = ArchitectureAgent(mock_brain, mock_graph_builder)
    agent.gateway = mock_gateway
    
    req = ProjectRequest(prompt="test", project_id="p1")
    req.discovery_data = {"domain": "analytics"}
    
    result = agent.generate_architecture(req)
    
    assert result is True
    mock_registry.get_learned_rules_for_domain.assert_called_with("analytics")
    
    # Verify the system prompt contains the learned rule
    called_args, called_kwargs = mock_gateway.generate.call_args
    system_prompt = called_kwargs.get("system_prompt", "")
    assert "LIÇÕES APRENDIDAS DE FALHAS ANTERIORES NESTE DOMÍNIO" in system_prompt
    assert "Bad architecture" in system_prompt
    assert "Use good architecture" in system_prompt
