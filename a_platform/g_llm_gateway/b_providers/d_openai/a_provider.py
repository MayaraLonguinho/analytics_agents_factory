import os
from typing import Any, AsyncGenerator, Dict, List
import openai
from a_platform.g_llm_gateway.f_interfaces.a_base_provider import BaseLLMProvider, LLMRequest, LLMResponse

class OpenAIProvider(BaseLLMProvider):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.name = "openai"
        api_key = self.config.get("api_key") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key is missing. No dummy keys allowed.")
        self._client = openai.AsyncOpenAI(api_key=api_key)

    async def health_check(self) -> bool:
        return True

    async def generate(self, request: LLMRequest) -> LLMResponse:
        try:
            response = await self._client.chat.completions.create(
                model=request.model,
                messages=[{"role": "user", "content": request.prompt}],
                max_tokens=request.max_tokens,
                temperature=request.temperature
            )
            content = response.choices[0].message.content
            return LLMResponse(content=content, model=request.model, provider=self.name)
        except Exception as e:
            raise ValueError(f"OpenAI error: {str(e)}")

    async def chat(self, messages: List[Dict[str, str]], model: str, **kwargs) -> LLMResponse:
        try:
            response = await self._client.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs
            )
            content = response.choices[0].message.content
            return LLMResponse(content=content, model=model, provider=self.name)
        except Exception as e:
            raise ValueError(f"OpenAI error: {str(e)}")

    async def structured_output(self, prompt: str, model: str, schema: Dict[str, Any], **kwargs) -> LLMResponse:
        # Fallback para response_format simplificado
        try:
            response = await self._client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                **kwargs
            )
            content = response.choices[0].message.content
            return LLMResponse(content=content, model=model, provider=self.name)
        except Exception as e:
            raise ValueError(f"OpenAI error: {str(e)}")

    async def embeddings(self, text: str, model: str, **kwargs) -> List[float]:
        try:
            response = await self._client.embeddings.create(input=[text], model=model)
            return response.data[0].embedding
        except Exception as e:
            raise ValueError(f"OpenAI error: {str(e)}")

    async def stream(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        response = await self._client.chat.completions.create(
            model=request.model,
            messages=[{"role": "user", "content": request.prompt}],
            stream=True
        )
        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
