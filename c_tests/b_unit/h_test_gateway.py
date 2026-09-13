import os
os.environ['OPENAI_API_KEY'] = 'sk-dummy'
os.environ['ANTHROPIC_API_KEY'] = 'sk-dummy'
os.environ['GEMINI_API_KEY'] = 'sk-dummy'

from a_platform.g_llm_gateway.e_gateway import LLMGateway
import pytest
from a_platform.a_core.c_exceptions.a_exceptions import ConfigurationError

def test_gateway_raises_on_dummy_key(monkeypatch):
    from a_platform.g_llm_gateway.b_providers.d_openai.a_provider import OpenAIProvider
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError):
        OpenAIProvider({"api_key": "", "enabled": True})
