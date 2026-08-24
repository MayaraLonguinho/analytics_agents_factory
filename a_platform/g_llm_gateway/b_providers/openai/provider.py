import os
import json
from typing import Optional, Type, Any
from a_platform.f_llm_gateway.a_interfaces.base_provider import BaseLLMProvider

try:
    import openai  # type: ignore
except ImportError:
    openai = None

class OpenAIProvider(BaseLLMProvider):
    async def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY não configurada. LLM = FAIL")
        if not openai:
            raise ImportError("Biblioteca 'openai' não instalada. LLM = FAIL")
            
        client = openai.AsyncOpenAI(api_key=api_key)
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = await client.chat.completions.create(
                model=kwargs.get("model", "gpt-4o-mini"),
                messages=messages,
                temperature=kwargs.get("temperature", 0.7)
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Falha na API OpenAI: {e}. LLM = FAIL")

    async def generate_structured(self, prompt: str, response_model: type, system_prompt: Optional[str] = None, **kwargs) -> Any:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY não configurada. LLM = FAIL")
        if not openai:
            raise ImportError("Biblioteca 'openai' não instalada. LLM = FAIL")
            
        client = openai.AsyncOpenAI(api_key=api_key)
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = await client.beta.chat.completions.parse(
                model=kwargs.get("model", "gpt-4o-mini"),
                messages=messages,
                response_format=response_model,
                temperature=kwargs.get("temperature", 0.0)
            )
            return response.choices[0].message.parsed
        except Exception as e:
            raise Exception(f"Falha na API OpenAI (Structured): {e}. LLM = FAIL")
