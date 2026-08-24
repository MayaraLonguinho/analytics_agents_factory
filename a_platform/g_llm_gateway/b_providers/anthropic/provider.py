import os
from typing import Optional, Type, Any
from a_platform.g_llm_gateway.a_interfaces.base_provider import BaseLLMProvider

try:
    import anthropic  # type: ignore
except ImportError:
    anthropic = None

class AnthropicProvider(BaseLLMProvider):
    async def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY não configurada. LLM = FAIL")
        if not anthropic:
            raise ImportError("Biblioteca 'anthropic' não instalada. LLM = FAIL")
            
        client = anthropic.AsyncAnthropic(api_key=api_key)
        
        try:
            response = await client.messages.create(
                model=kwargs.get("model", "claude-3-5-sonnet-20240620"),
                max_tokens=kwargs.get("max_tokens", 4096),
                temperature=kwargs.get("temperature", 0.7),
                system=system_prompt or "",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Falha na API Anthropic: {e}. LLM = FAIL")

    async def generate_structured(self, prompt: str, response_model: type, system_prompt: Optional[str] = None, **kwargs) -> Any:
        raise NotImplementedError("Structured generation not fully implemented for Anthropic in this version. LLM = FAIL")
