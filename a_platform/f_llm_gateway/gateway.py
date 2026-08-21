from typing import Optional, Type, Dict
from pydantic import BaseModel
from a_platform.f_llm_gateway.a_interfaces.base_provider import BaseLLMProvider
from a_platform.f_llm_gateway.b_providers.ollama.provider import OllamaProvider
from a_platform.f_llm_gateway.b_providers.openai.provider import OpenAIProvider
from a_platform.f_llm_gateway.b_providers.anthropic.provider import AnthropicProvider
from a_platform.f_llm_gateway.b_providers.google.provider import GoogleProvider
from a_platform.f_llm_gateway.d_routing.router import LLMRouter

class LLMGateway:
    def __init__(self):
        self.router = LLMRouter()
        self.providers: Dict[str, BaseLLMProvider] = {
            "ollama": OllamaProvider(),
            "openai": OpenAIProvider(),
            "anthropic": AnthropicProvider(),
            "google": GoogleProvider()
        }
        
    async def generate(self, prompt: str, complexity: str = "low", system_prompt: Optional[str] = None, **kwargs) -> str:
        provider_name = self.router.route(complexity)
        provider = self.providers.get(provider_name, self.providers["ollama"])
        return await provider.generate(prompt, system_prompt, **kwargs)
        
    async def generate_structured(self, prompt: str, response_model: Type[BaseModel], complexity: str = "low", system_prompt: Optional[str] = None, **kwargs) -> BaseModel:
        provider_name = self.router.route(complexity)
        provider = self.providers.get(provider_name, self.providers["ollama"])
        return await provider.generate_structured(prompt, response_model, system_prompt, **kwargs)
