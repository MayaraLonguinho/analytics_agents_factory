"""
c_tests/b_system/a_planning/b_test_capability_routing.py
======================================================
Especificação executável de roteamento de capabilities via SkillIndex e SkillRouter.
Valida que cada capability demandada no plano é mapeada para uma skill homologada.
"""
import pytest

from a_platform.e_skills.skill_index import SkillIndex
from a_platform.e_skills.skill_router import SkillRouter


def test_capability_routing_end_to_end():
    """Valida o ciclo completo: consulta no índice leve -> resolução determinística pelo router."""
    index = SkillIndex.get_instance()
    router = SkillRouter(skill_index=index)

    # Capabilities analíticas típicas
    requested_capabilities = [
        "data-ingestion",
        "data-cleaning",
        "exploratory-data-analysis",
    ]

    plan = router.route_skills(requested_capabilities)
    assert len(plan) == 3
    selected_skill_ids = [item.skill_id for item in plan]
    assert "data-ingestion" in selected_skill_ids
    assert "data-cleaning" in selected_skill_ids
    assert "exploratory-data-analysis" in selected_skill_ids
