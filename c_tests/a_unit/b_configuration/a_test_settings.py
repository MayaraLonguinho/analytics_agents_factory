"""
c_tests/a_unit/b_configuration/a_test_settings.py
===============================================
Especificação executável de g_configuration.
Valida estritamente provedores suportados, normalização, ausência de fallback silencioso,
limites de timeout, tentativas de repair e a API pública.
"""
import pytest
from pydantic import ValidationError

from g_configuration import AAFSettings, Settings, get_settings, settings
from g_configuration.a_settings import SUPPORTED_LLM_PROVIDERS


def test_settings_public_api():
    """Valida a consistência e integridade da API pública exportada por g_configuration."""
    assert Settings is AAFSettings
    assert isinstance(settings, AAFSettings)
    fresh_settings = get_settings()
    assert isinstance(fresh_settings, AAFSettings)


def test_settings_default_values():
    """Valida os valores operacionais padrão legítimos do AAF."""
    s = AAFSettings()
    assert s.llm_provider == "openai"
    assert s.llm_model == "gpt-4o-mini"
    assert s.command_timeout_seconds == 120.0
    assert s.max_repair_attempts == 3
    assert s.openai_api_key == ""
    assert s.anthropic_api_key == ""
    assert s.gemini_api_key == ""


def test_settings_supported_providers_set():
    """Garante que apenas os provedores homologados estão no conjunto suportado."""
    assert SUPPORTED_LLM_PROVIDERS == frozenset({"openai", "anthropic", "gemini"})


@pytest.mark.parametrize("provider", ["openai", "anthropic", "gemini"])
def test_settings_supported_providers_accepted(provider):
    """Valida que todos os provedores homologados são aceitos."""
    s = AAFSettings(llm_provider=provider)
    assert s.llm_provider == provider


def test_settings_provider_normalization():
    """Valida que entradas com espaços ou caixa mista são normalizadas com strip e lower."""
    s1 = AAFSettings(llm_provider="  OpenAI  ")
    assert s1.llm_provider == "openai"

    s2 = AAFSettings(llm_provider="ANTHROPIC")
    assert s2.llm_provider == "anthropic"

    s3 = AAFSettings(llm_provider="  Gemini ")
    assert s3.llm_provider == "gemini"


def test_settings_invalid_provider_raises_explicit_validation_error():
    """
    CRÍTICO: Valida que um provedor não suportado levanta ValidationError imediata.
    É estritamente proibido aplicar fallback silencioso para 'openai'.
    """
    with pytest.raises(ValidationError) as exc_info:
        AAFSettings(llm_provider="unsupported_custom_provider")
    
    error_msg = str(exc_info.value)
    assert "Provedor LLM inválido" in error_msg
    assert "openai" in error_msg
    assert "anthropic" in error_msg
    assert "gemini" in error_msg


def test_settings_command_timeout_bounds():
    """Valida que command_timeout_seconds deve ser no mínimo 1.0 segundo."""
    s = AAFSettings(command_timeout_seconds=1.0)
    assert s.command_timeout_seconds == 1.0

    with pytest.raises(ValidationError):
        AAFSettings(command_timeout_seconds=0.5)


def test_settings_max_repair_attempts_bounds():
    """Valida os limites mínimo (1) e máximo (10) de max_repair_attempts."""
    s_min = AAFSettings(max_repair_attempts=1)
    assert s_min.max_repair_attempts == 1

    s_max = AAFSettings(max_repair_attempts=10)
    assert s_max.max_repair_attempts == 10

    with pytest.raises(ValidationError):
        AAFSettings(max_repair_attempts=0)

    with pytest.raises(ValidationError):
        AAFSettings(max_repair_attempts=11)


def test_settings_environment_variable_override(monkeypatch):
    """Valida a precedência de variáveis de ambiente sobre defaults."""
    monkeypatch.setenv("LLM_PROVIDER", "anthropic")
    monkeypatch.setenv("COMMAND_TIMEOUT_SECONDS", "300.0")
    monkeypatch.setenv("MAX_REPAIR_ATTEMPTS", "5")

    s = AAFSettings()
    assert s.llm_provider == "anthropic"
    assert s.command_timeout_seconds == 300.0
    assert s.max_repair_attempts == 5
