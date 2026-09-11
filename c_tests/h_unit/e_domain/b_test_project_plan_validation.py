# pyrefly: ignore [missing-import]
import pytest
from unittest.mock import MagicMock
from a_platform.a_core.b_domain.project_plan import ProjectPlan, Task

def get_mocks():
    skill_registry = MagicMock()
    skill_registry.get_skill.side_effect = lambda s: True if s == "valid_skill" else False
    
    mcp_registry = MagicMock()
    mcp_registry.get_tool.side_effect = lambda m: True if m == "valid_mcp" else False
    
    agent_factory = MagicMock()
    agent_factory.get_agent.side_effect = lambda a: True if a == "valid_agent" else False
    
    validation_gate = MagicMock()
    validation_gate.has_validator.side_effect = lambda v: True if v == "valid_validator" else False
    
    return skill_registry, mcp_registry, agent_factory, validation_gate

def test_validate_full_success():
    skill_registry, mcp_registry, agent_factory, validation_gate = get_mocks()
    
    plan = ProjectPlan(project_id="p1", domain="test")
    plan.add_task(Task(
        id="t1",
        name="Task 1",
        description="Desc",
        agent="valid_agent",
        skills=["valid_skill"],
        mcps=["valid_mcp"],
        validators=["valid_validator"],
        expected_artifacts=["file.txt"]
    ))
    
    assert plan.validate_full(skill_registry, mcp_registry, agent_factory, validation_gate) is True
    assert plan.validated is True

def test_validate_full_invalid_agent():
    skill_registry, mcp_registry, agent_factory, validation_gate = get_mocks()
    
    plan = ProjectPlan(project_id="p1", domain="test")
    plan.add_task(Task(
        id="t1",
        name="Task 1",
        description="Desc",
        agent="invalid_agent",
        expected_artifacts=["file.txt"]
    ))
    
    with pytest.raises(ValueError, match="Agente inválido"):
        plan.validate_full(skill_registry, mcp_registry, agent_factory, validation_gate)

def test_validate_full_invalid_skill():
    skill_registry, mcp_registry, agent_factory, validation_gate = get_mocks()
    
    plan = ProjectPlan(project_id="p1", domain="test")
    plan.add_task(Task(
        id="t1",
        name="Task 1",
        description="Desc",
        agent="valid_agent",
        skills=["invalid_skill"],
        expected_artifacts=["file.txt"]
    ))
    
    with pytest.raises(ValueError, match="Skill não registrada"):
        plan.validate_full(skill_registry, mcp_registry, agent_factory, validation_gate)

def test_validate_full_invalid_mcp():
    skill_registry, mcp_registry, agent_factory, validation_gate = get_mocks()
    
    plan = ProjectPlan(project_id="p1", domain="test")
    plan.add_task(Task(
        id="t1",
        name="Task 1",
        description="Desc",
        agent="valid_agent",
        mcps=["invalid_mcp"],
        expected_artifacts=["file.txt"]
    ))
    
    with pytest.raises(ValueError, match="MCP não registrado"):
        plan.validate_full(skill_registry, mcp_registry, agent_factory, validation_gate)

def test_validate_full_invalid_validator():
    skill_registry, mcp_registry, agent_factory, validation_gate = get_mocks()
    
    plan = ProjectPlan(project_id="p1", domain="test")
    plan.add_task(Task(
        id="t1",
        name="Task 1",
        description="Desc",
        agent="valid_agent",
        validators=["invalid_validator"],
        expected_artifacts=["file.txt"]
    ))
    
    with pytest.raises(ValueError, match="Validator não reconhecido"):
        plan.validate_full(skill_registry, mcp_registry, agent_factory, validation_gate)

def test_validate_full_invalid_artifact():
    skill_registry, mcp_registry, agent_factory, validation_gate = get_mocks()
    
    plan = ProjectPlan(project_id="p1", domain="test")
    plan.add_task(Task(
        id="t1",
        name="Task 1",
        description="Desc",
        agent="valid_agent",
        expected_artifacts=["invalid_artifact_no_extension"]
    ))
    
    with pytest.raises(ValueError, match="Formato de artefato inválido"):
        plan.validate_full(skill_registry, mcp_registry, agent_factory, validation_gate)
