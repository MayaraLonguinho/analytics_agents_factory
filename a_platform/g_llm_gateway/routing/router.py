from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class RouteDecision:
    provider: str
    model: str
    metadata: Dict[str, Any]


class ModelRouter:
    """Routes requests to a provider/model combination."""

    def __init__(self, provider_map: Optional[Dict[str, Dict[str, Any]]] = None):
        self.provider_map = provider_map or {
            "ollama": {"model": "qwen3:4b", "metadata": {"provider": "ollama", "type": "local"}},
            "openai": {"model": "gpt-4o-mini", "metadata": {"provider": "openai", "type": "cloud"}},
            "anthropic": {"model": "claude-3-haiku", "metadata": {"provider": "anthropic", "type": "cloud"}},
            "google": {"model": "gemini-1.5-flash", "metadata": {"provider": "google", "type": "cloud"}},
        }

    def route(self, provider: Optional[str] = None, model: Optional[str] = None) -> RouteDecision:
        selected_provider = provider or "ollama"
        selected_model = model or self.provider_map[selected_provider]["model"]
        return RouteDecision(
            provider=selected_provider,
            model=selected_model,
            metadata={**self.provider_map.get(selected_provider, {}).get("metadata", {}), "requested_provider": selected_provider},
        )
