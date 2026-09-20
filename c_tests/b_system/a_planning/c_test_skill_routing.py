"""
c_tests/b_system/a_planning/c_test_skill_routing.py
=================================================
Especificação executável de Skill Routing com guardrails de domínio e agentes.
Valida que skills são roteadas respeitando restrições e compatibilidade de agentes.
"""
import pytest

from a_platform.e_skills.skill_router import SkillRouter, SkillRoutingError


def test_skill_routing_with_agent_compatibility():
    """Valida que o router seleciona skills compatíveis com o agente responsável."""
    router = SkillRouter()
    # DataAgent executando data-ingestion
    skill = router.route_skill("data-ingestion", agent="DataAgent")
    assert skill == "data-ingestion"


def test_skill_routing_preferred_skill_resolution():
    """Valida que preferred_skill é priorizada quando declarada na task."""
    router = SkillRouter()
    skill = router.route_skill("data-ingestion", preferred_skill="data-ingestion")
    assert skill == "data-ingestion"
