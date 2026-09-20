"""
c_tests/a_unit/c_brain/b_test_rules.py
====================================
Especificação executável das regras de engenharia e papéis do Brain.
Valida regras de separação de responsabilidades (SoC), coesão, segurança e papéis.
"""
import pytest

from a_platform.c_brain import Brain


def test_brain_architecture_rules():
    """Valida as regras fundamentais de arquitetura registradas no Brain."""
    brain = Brain()
    arch_rules = brain.get_rules("architecture")
    assert isinstance(arch_rules, list)
    assert len(arch_rules) >= 3


def test_brain_security_rules():
    """Valida as regras essenciais de segurança registradas no Brain."""
    brain = Brain()
    sec_rules = brain.get_rules("security")
    assert isinstance(sec_rules, list)
    assert len(sec_rules) >= 2


def test_brain_role_rules():
    """Valida as definições de papéis de agentes da fábrica."""
    brain = Brain()
    roles = brain.get_rules("role")
    assert isinstance(roles, list)
    assert len(roles) >= 5
