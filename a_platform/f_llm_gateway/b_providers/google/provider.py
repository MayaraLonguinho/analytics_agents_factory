import os
from typing import Optional, Type, Any
from a_platform.f_llm_gateway.a_interfaces.base_provider import BaseLLMProvider

try:
    import google.generativeai as genai  # type: ignore
except ImportError:
    genai = None

class GoogleProvider(BaseLLMProvider):
    async def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY não configurada. LLM = FAIL")
        if not genai:
            raise ImportError("Biblioteca 'google.generativeai' não instalada. LLM = FAIL")
            
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(kwargs.get("model", "gemini-1.5-flash"))
        
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"SYSTEM: {system_prompt}\n\nUSER: {prompt}"
            
        try:
            response = await model.generate_content_async(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=kwargs.get("temperature", 0.7)
                )
            )
            return response.text
        except Exception as e:
            raise Exception(f"Falha na API Google: {e}. LLM = FAIL")

    async def generate_structured(self, prompt: str, response_model: type, system_prompt: Optional[str] = None, **kwargs) -> Any:
        raise NotImplementedError("Structured generation not fully implemented for Google in this version. LLM = FAIL")
