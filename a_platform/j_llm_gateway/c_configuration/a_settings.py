from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class LLMGatewayConfig:
    default_provider: str = "openai"
    default_model: str = "gpt-4o-mini"
    providers: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "openai": {
            "base_url": "https://api.openai.com/v1",
            "supported_models": ["gpt-4o-mini"],
            "enabled": True,
        },
        "anthropic": {
            "base_url": "https://api.anthropic.com",
            "supported_models": ["claude-3-haiku"],
            "enabled": False,
        },
        "gemini": {
            "base_url": "https://generativelanguage.googleapis.com",
            "supported_models": ["gemini-1.5-flash"],
            "enabled": False,
        },
    })
