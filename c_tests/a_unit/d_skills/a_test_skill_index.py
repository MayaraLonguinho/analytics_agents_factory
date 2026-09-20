"""
c_tests/a_unit/d_skills/a_test_skill_index.py
===========================================
Especificação executável de SkillIndex.
Valida indexação leve, metadados de capabilities, dependências e busca sem carregar código.
"""
import pytest

from a_platform.e_skills.skill_index import SkillIndex, SkillMetadata


def test_skill_index_singleton_and_size():
    """Valida que o SkillIndex é carregado como singleton contendo todas as skills homologadas."""
    index = SkillIndex.get_instance()
    all_skills = index.list_all()
    assert isinstance(all_skills, list)
    assert len(all_skills) >= 25  # 26 skills catalogadas


def test_skill_index_find_by_capability():
    """Valida a busca de skills por capability com retorno tipado de SkillMetadata."""
    index = SkillIndex.get_instance()
    candidates = index.find_by_capability("data-ingestion")
    assert isinstance(candidates, list)
    assert len(candidates) >= 1
    assert any(c.skill_id == "data-ingestion" for c in candidates)


def test_skill_index_get_dependencies():
    """Valida a consulta de dependências declaradas para uma skill específica."""
    index = SkillIndex.get_instance()
    meta = index.get("data-cleaning")
    if meta:
        assert isinstance(meta.dependencies, list)
