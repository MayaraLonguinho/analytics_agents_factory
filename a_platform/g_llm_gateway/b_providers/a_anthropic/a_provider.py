import os
from typing import Any, AsyncGenerator, Dict, List
from a_platform.g_llm_gateway.f_interfaces.a_base_provider import BaseLLMProvider, LLMRequest, LLMResponse

class AnthropicProvider(BaseLLMProvider):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.name = "anthropic"
        api_key = self.config.get("api_key") or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Anthropic API key is missing. No dummy keys allowed.")

    async def generate(self, request: LLMRequest) -> LLMResponse:
        raise ValueError("Anthropic SDK not fully wrapped yet. Cannot return dummy success.")

    async def chat(self, messages: List[Dict[str, str]], model: str, **kwargs) -> LLMResponse:
        raise ValueError("Anthropic SDK not fully wrapped yet. Cannot return dummy success.")

    async def structured_output(self, prompt: str, model: str, schema: Dict[str, Any], **kwargs) -> LLMResponse:
        raise ValueError("Anthropic SDK not fully wrapped yet. Cannot return dummy success.")

    async def embeddings(self, text: str, model: str, **kwargs) -> List[float]:
        raise ValueError("Anthropic SDK not fully wrapped yet. Cannot return dummy success.")

    async def stream(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        raise ValueError("Anthropic SDK not fully wrapped yet. Cannot return dummy success.")
        yield ""
