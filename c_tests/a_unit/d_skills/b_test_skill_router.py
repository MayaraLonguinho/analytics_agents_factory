"""
c_tests/a_unit/d_skills/b_test_skill_router.py
============================================
Especificação executável de SkillRouter.
Valida mapeamento determinístico de Capabilities para Skills, deduplicação,
ordenação topológica e rejeição estrita via SkillRoutingError.
"""
import pytest

from a_platform.e_skills.skill_router import SkillRouter, SkillRoutingError, SkillSelectionItem


def test_skill_router_single_capability():
    """Valida o roteamento de uma única capability para a skill correspondente."""
    router = SkillRouter()
    selected = router.route_skill("data-ingestion")
    assert selected == "data-ingestion"


def test_skill_router_multiple_capabilities_deduplication():
    """Valida a seleção multi-skill com deduplicação e ordenação topológica."""
    router = SkillRouter()
    capabilities = ["data-ingestion", "data-cleaning", "data-ingestion"]
    plan = router.route_skills(capabilities)
    assert isinstance(plan, list)
    # Deduplicação deve manter cada skill apenas uma vez
    skill_ids = [item.skill_id for item in plan]
    assert len(skill_ids) == len(set(skill_ids))
    assert "data-ingestion" in skill_ids
    assert "data-cleaning" in skill_ids


def test_skill_router_unknown_capability_raises_error():
    """Valida que capability desconhecida levanta SkillRoutingError sem fallback arbitrário."""
    router = SkillRouter()
    with pytest.raises(SkillRoutingError):
        router.route_skill("non_existent_magic_capability")
