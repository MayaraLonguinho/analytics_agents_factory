"""
c_tests/a_unit/c_brain/a_test_brain.py
====================================
Especificação executável do Brain da AAF.
Valida recuperação de conhecimento, regras de equipe, metadata de skills
e especifica que o padrão arquitetural normativo deve ser Modular Monolith.
"""
import pytest

from a_platform.c_brain import Brain


def test_brain_initialization():
    """Valida a inicialização dos registros e componentes do Brain."""
    brain = Brain()
    assert brain.domain_registry is not None
    assert brain.mcp_registry is not None
    assert brain.skill_index is not None
    assert brain.agent_registry is not None


def test_brain_team_standards():
    """Valida que o Brain carrega regras e padrões de equipe."""
    brain = Brain()
    team_standards = brain.get_rules("team_standard")
    assert isinstance(team_standards, list)
    assert len(team_standards) > 0


def test_brain_context_pack_generation():
    """Valida a geração de ContextPack com injeção de standards e metadados."""
    brain = Brain()
    context_req = {
        "project_type": "Analytics Pipeline",
        "domain": "analytics",
        "business_context": "Sales analysis",
        "capabilities": ["data-ingestion"],
    }
    pack = brain.generate_context_pack(context_req)
    assert "project" in pack
    assert pack["project"]["domain"] == "analytics"
    assert "team_standards" in pack
    assert "architecture" in pack


def test_brain_skills_compact_metadata():
    """Valida que o Brain expõe metadata compacta de skills indexadas."""
    brain = Brain()
    metadata = brain.get_skills_compact_metadata()
    assert isinstance(metadata, list)
    assert len(metadata) >= 20  # Espera-se ~26 skills indexadas
