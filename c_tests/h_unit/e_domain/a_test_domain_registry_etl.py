# pyrefly: ignore [missing-import]
import pytest
from a_platform.i_domains.domain_registry import DomainRegistry

@pytest.fixture
def registry():
    return DomainRegistry()

def test_etl_alias_resolution(registry):
    # Test 1 - alias ETL
    assert registry.normalize_domain("etl") == "data_engineering"
    
    # Test 2 - data pipeline
    assert registry.normalize_domain("data pipeline") == "data_engineering"
    
    # Test 3 - data engineering
    assert registry.normalize_domain("data engineering") == "data_engineering"
    
    # Test 4 - canonical domain
    assert registry.normalize_domain("data_engineering") == "data_engineering"

def test_unknown_domain_fails_explicitly(registry):
    # Test 5 - domínio realmente desconhecido
    with pytest.raises(ValueError, match="estritamente não suportado pela Factory"):
        registry.get_domain_config("dominio_invalido_123")

def test_generic_fallback_not_applied(registry):
    # Ensure it doesn't return generic for something unknown
    assert registry.normalize_domain("unknown_domain") == "unknown_domain"
    
def test_all_data_engineering_aliases(registry):
    aliases = [
        "etl", "etl pipeline", "data pipeline", "pipeline de dados",
        "data engineering", "engenharia de dados", "pipeline de ingestão",
        "pipeline de transformação", "pipeline de carga",
        "ingestão transformação carga", "extract transform load",
        "extract-transform-load"
    ]
    for alias in aliases:
        assert registry.normalize_domain(alias) == "data_engineering"
