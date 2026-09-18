from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, AsyncGenerator, Dict, List, Optional


@dataclass
class LLMRequest:
    prompt: str
    model: str
    parameters: Optional[Dict[str, Any]] = None
    stream: bool = False
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    messages: Optional[List[Dict[str, str]]] = None
    response_format: Optional[Dict[str, Any]] = None


@dataclass
class LLMResponse:
    content: str
    model: str
    provider: str
    tokens_used: Optional[int] = None
    finish_reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseLLMProvider(ABC):
    """Base interface for all LLM providers."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider_name = self.__class__.__name__

    @abstractmethod
    async def generate(self, request: LLMRequest) -> LLMResponse:
        raise NotImplementedError

    @abstractmethod
    async def chat(self, messages: List[Dict[str, str]], model: str, **kwargs) -> LLMResponse:
        raise NotImplementedError

    @abstractmethod
    async def structured_output(self, prompt: str, model: str, schema: Dict[str, Any], **kwargs) -> LLMResponse:
        raise NotImplementedError

    @abstractmethod
    async def embeddings(self, text: str, model: str, **kwargs) -> List[float]:
        raise NotImplementedError

    @abstractmethod
    async def stream(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        raise NotImplementedError

    def get_supported_models(self) -> List[str]:
        return self.config.get("supported_models", [])
