import pytest
from typing import Dict, Any

from a_platform.c_brain.h_brain import Brain
from a_platform.a_core.d_session.b_context import ExecutionContext, Decision

def test_carregamento_do_brain():
    brain = Brain()
    assert brain.rule_registry is not None
    assert brain.knowledge_registry is not None
    assert brain.pattern_registry is not None

def test_leitura_de_rules():
    brain = Brain()
    rules = brain.get_rules("team_standard")
    
    # Valida regras críticas
    assert any("Não inventar regra de negócio" in rule for rule in rules)
    assert any("NENHUMA circunstância" in rule for rule in rules)

def test_leitura_de_context():
    brain = Brain()
    req = {
        "domain": "data_engineering",
        "project_type": "Data Pipeline",
        "fetch_platform_stack": False
    }
    
    pack = brain.generate_context_pack(req)
    
    assert "project" in pack
    assert pack["project"]["domain"] == "data_engineering"
    assert "team_standards" in pack
    
    # Como não pedimos fetch_platform_stack, a stack da plataforma não deve estar presente no pack padrão (ou estar vazia)
    assert "platform_stack" not in pack or not pack["platform_stack"]

def test_criacao_de_decision():
    context = ExecutionContext()
    decision = Decision(id="D-001", status="adopted", decision="Usar Snowflake", reason="Default inteligente")
    context.add_decision(decision)
    
    assert len(context.decisions) == 1
    assert context.decisions[0].id == "D-001"
    assert context.decisions[0].decision == "Usar Snowflake"

def test_consulta_de_knowledge():
    brain = Brain()
    # Verifica knowledge on demand
    req = {
        "domain": "analytics",
        "fetch_platform_stack": True
    }
    pack = brain.generate_context_pack(req)
    
    assert "platform_stack" in pack
    # A platform_stack deve conter informações preenchidas pois pedimos
    assert len(pack["platform_stack"]) > 0
