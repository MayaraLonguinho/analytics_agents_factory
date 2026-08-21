from typing import Optional, Type
from pydantic import BaseModel
from a_platform.f_llm_gateway.a_interfaces.base_provider import BaseLLMProvider

class OpenAIProvider(BaseLLMProvider):
    async def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        return "OpenAI mocked response"
        
    async def generate_structured(self, prompt: str, response_model: Type[BaseModel], system_prompt: Optional[str] = None, **kwargs) -> BaseModel:
        return response_model()
