from __future__ import annotations

from typing import Any, AsyncGenerator, Dict, List, Optional

from .d_configuration.a_settings import LLMGatewayConfig
from .f_interfaces.a_base_provider import BaseLLMProvider, LLMRequest, LLMResponse
from .b_providers import AnthropicProvider, GeminiProvider, OpenAIProvider, get_provider_registry
from .b_providers.e_registry import ProviderRegistry
from .g_routing.a_router import ModelRouter


class LLMGateway:
    """Canonical gateway for all LLM access in the platform.

    Agent -> Skill -> LLM Gateway -> Provider -> Model
    """

    def __init__(self, config: Optional[LLMGatewayConfig] = None):
        self.config = config or LLMGatewayConfig()
        self.router = ModelRouter()
        self.e_registry: ProviderRegistry = get_provider_registry()
        self._initialize_providers()

    def _initialize_providers(self) -> None:
        provider_defs = self.config.providers
        provider_map = {
            "openai": OpenAIProvider,
            "anthropic": AnthropicProvider,
            "gemini": GeminiProvider,
        }

        for name, cfg in provider_defs.items():
            if not cfg.get("enabled", False):
                continue
            provider_cls = provider_map.get(name)
            if provider_cls is None:
                continue
            provider = provider_cls(cfg)
            self.e_registry.register_provider(name, provider, cfg)

    def route(self, provider: Optional[str] = None, model: Optional[str] = None):
        return self.router.route(provider=provider, model=model)

    async def generate(self, prompt: str, provider: Optional[str] = None, model: Optional[str] = None, **kwargs) -> LLMResponse:
        route = self.route(provider=provider, model=model)
        provider_instance = self.e_registry.get_provider(route.provider)
        if provider_instance is None:
            raise ValueError(f"Provider not available: {route.provider}")

        request = LLMRequest(
            prompt=prompt,
            model=route.model,
            parameters=kwargs,
            stream=kwargs.get("stream", False),
            max_tokens=kwargs.get("max_tokens"),
            temperature=kwargs.get("temperature"),
        )
        return await provider_instance.generate(request)

    async def chat(self, messages: List[Dict[str, str]], provider: Optional[str] = None, model: Optional[str] = None, **kwargs) -> LLMResponse:
        route = self.route(provider=provider, model=model)
        provider_instance = self.e_registry.get_provider(route.provider)
        if provider_instance is None:
            raise ValueError(f"Provider not available: {route.provider}")
        return await provider_instance.chat(messages, route.model, **kwargs)

    async def structured_output(self, prompt: str, schema: Dict[str, Any], provider: Optional[str] = None, model: Optional[str] = None, **kwargs) -> LLMResponse:
        route = self.route(provider=provider, model=model)
        provider_instance = self.e_registry.get_provider(route.provider)
        if provider_instance is None:
            raise ValueError(f"Provider not available: {route.provider}")
        return await provider_instance.structured_output(prompt, route.model, schema, **kwargs)

    async def embeddings(self, text: str, provider: Optional[str] = None, model: Optional[str] = None, **kwargs) -> List[float]:
        route = self.route(provider=provider, model=model)
        provider_instance = self.e_registry.get_provider(route.provider)
        if provider_instance is None:
            raise ValueError(f"Provider not available: {route.provider}")
        return await provider_instance.embeddings(text, route.model, **kwargs)

    async def stream(self, prompt: str, provider: Optional[str] = None, model: Optional[str] = None, **kwargs) -> AsyncGenerator[str, None]:
        route = self.route(provider=provider, model=model)
        provider_instance = self.e_registry.get_provider(route.provider)
        if provider_instance is None:
            raise ValueError(f"Provider not available: {route.provider}")
        request = LLMRequest(
            prompt=prompt,
            model=route.model,
            parameters=kwargs,
            stream=True,
            max_tokens=kwargs.get("max_tokens"),
            temperature=kwargs.get("temperature"),
        )
        async for chunk in provider_instance.stream(request):
            yield chunk

    def metadata(self) -> Dict[str, Any]:
        return {
            "default_provider": self.config.default_provider,
            "default_model": self.config.default_model,
            "providers": {name: cfg for name, cfg in self.config.providers.items()},
            "routing": {"default": self.route().provider, "model": self.route().model},
        }
