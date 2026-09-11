from __future__ import annotations

from typing import Any, AsyncGenerator, Dict, List

from ...f_interfaces.a_base_provider import BaseLLMProvider, LLMRequest, LLMResponse


class OllamaProvider(BaseLLMProvider):
    """Official Ollama provider for local model execution."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get("base_url", "http://localhost:11434")
        self._client = None
        self._initialize_client()

    def _initialize_client(self) -> None:
        try:
            from ollama import AsyncClient

            self._client = AsyncClient(host=self.base_url)
        except ImportError as exc:  # pragma: no cover
            raise ImportError("Ollama SDK not installed. Install via pip install ollama") from exc

    async def generate(self, request: LLMRequest) -> LLMResponse:
        response = await self._client.generate(
            model=request.model,
            prompt=request.prompt,
            options={
                "temperature": request.temperature if request.temperature is not None else 0.7,
                "num_predict": request.max_tokens if request.max_tokens is not None else 512,
                **(request.parameters or {}),
            },
            stream=request.stream,
        )
        if request.stream:
            return LLMResponse(
                content="",
                model=request.model,
                provider="ollama",
                metadata={"streaming": True, "response": response},
            )
        return LLMResponse(
            content=response.get("response", ""),
            model=request.model,
            provider="ollama",
            tokens_used=response.get("eval_count", 0) + response.get("prompt_eval_count", 0),
            finish_reason=response.get("done_reason"),
            metadata={"total_duration": response.get("total_duration")},
        )

    async def chat(self, messages: List[Dict[str, str]], model: str, **kwargs) -> LLMResponse:
        response = await self._client.chat(model=model, messages=messages, **kwargs)
        message = response.get("message", {})
        return LLMResponse(
            content=message.get("content", ""),
            model=model,
            provider="ollama",
            tokens_used=response.get("eval_count", 0) + response.get("prompt_eval_count", 0),
            finish_reason=response.get("done_reason"),
            metadata=response.get("meta", {}),
        )

    async def structured_output(self, prompt: str, model: str, schema: Dict[str, Any], **kwargs) -> LLMResponse:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt + "\nReturn valid JSON matching this schema: " + str(schema)}],
            "format": schema,
            **kwargs,
        }
        response = await self._client.chat(**payload)
        content = response.get("message", {}).get("content", "")
        return LLMResponse(content=content, model=model, provider="ollama", metadata={"structured_output": True})

    async def embeddings(self, text: str, model: str, **kwargs) -> List[float]:
        response = await self._client.embeddings(model=model, input=text, **kwargs)
        return response.get("embedding", [])

    async def stream(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        stream = await self._client.generate(model=request.model, prompt=request.prompt, stream=True, options={
            "temperature": request.temperature if request.temperature is not None else 0.7,
            "num_predict": request.max_tokens if request.max_tokens is not None else 512,
            **(request.parameters or {}),
        })
        async for chunk in stream:
            if chunk.get("response"):
                yield chunk["response"]

    async def health_check(self) -> bool:
        try:
            await self._client.list()
            return True
        except Exception:
            return False
