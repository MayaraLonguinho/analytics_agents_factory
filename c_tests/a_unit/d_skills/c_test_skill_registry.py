"""
c_tests/a_unit/d_skills/c_test_skill_registry.py
==============================================
Especificação executável de SkillRegistry.
Valida o carregamento sob demanda (lazy loading) e resolução de instâncias concretas de skills.
"""
import pytest

from a_platform.e_skills.skill_registry import SkillRegistry
from a_platform.b_contracts.c_skill_contract import BaseSkill


def test_skill_registry_lazy_load_canonical():
    """Valida a resolução de skill por ID canônico kebab-case."""
    registry = SkillRegistry()
    skill = registry.get_skill("dataset-profiling")
    assert isinstance(skill, BaseSkill)
    assert skill.skill_id == "dataset-profiling"


def test_skill_registry_lazy_load_legacy_alias():
    """Valida suporte a aliases legados snake_case."""
    registry = SkillRegistry()
    skill = registry.get_skill("dataset_profiling")
    assert isinstance(skill, BaseSkill)
    assert skill.skill_id == "dataset-profiling"


def test_skill_registry_caching():
    """Valida que instâncias já carregadas são cacheadas em memória."""
    registry = SkillRegistry()
    skill1 = registry.get_skill("data-cleaning")
    skill2 = registry.get_skill("data-cleaning")
    assert skill1 is skill2


def test_skill_registry_nonexistent_skill_raises_error():
    """Valida que requisição de skill não cadastrada gera KeyError ou erro explícito."""
    registry = SkillRegistry()
    with pytest.raises((KeyError, ValueError)):
        registry.get_skill("nonexistent-ghost-skill")
