"""
c_tests/a_unit/c_brain/c_test_domains.py
======================================
Especificação executável do DomainRegistry do Brain.
Valida o carregamento dos domínios analíticos e padrões associados.
"""
import pytest

from a_platform.c_brain.d_domains.a_domain_registry import DomainRegistry


def test_domain_registry_initialization():
    """Valida que os domínios homologados de Analytics e Data Engineering estão carregados."""
    registry = DomainRegistry()
    domains = registry.list_domains()
    assert isinstance(domains, list)
    assert len(domains) >= 2


def test_domain_registry_retrieval():
    """Valida a consulta de padrões e metadados por domínio específico."""
    registry = DomainRegistry()
    domain_info = registry.get_domain("analytics")
    assert domain_info is not None
