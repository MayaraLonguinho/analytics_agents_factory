from __future__ import annotations

from typing import Any, Dict, Optional

from ..interfaces.base_provider import BaseLLMProvider


class ProviderRegistry:
    """Registry for all configured providers."""

    def __init__(self):
        self._providers: Dict[str, BaseLLMProvider] = {}
        self._configs: Dict[str, Dict[str, Any]] = {}

    def register_provider(self, name: str, provider: BaseLLMProvider, config: Dict[str, Any]) -> None:
        self._providers[name] = provider
        self._configs[name] = config

    def get_provider(self, name: str) -> Optional[BaseLLMProvider]:
        return self._providers.get(name)

    def get_config(self, name: str) -> Optional[Dict[str, Any]]:
        return self._configs.get(name)

    def list_providers(self) -> list[str]:
        return list(self._providers.keys())


def get_provider_registry() -> ProviderRegistry:
    return _GLOBAL_PROVIDER_REGISTRY


_GLOBAL_PROVIDER_REGISTRY = ProviderRegistry()
