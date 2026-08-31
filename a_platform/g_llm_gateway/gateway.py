import logging
import os
import urllib.request
import urllib.parse
import json
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LLMGateway:
    """
    Gateway real de LLMs com roteamento e fallback estrito.
    Não aceita mocks. Falha se não houver chaves configuradas.
    Suporta OpenAI e Google Gemini nativamente via API HTTP.
    """
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.google_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        
    def generate(self, prompt: str, system_prompt: str = "", model_preference: str = "openai", **kwargs) -> Dict[str, Any]:
        logger.info(f"[LLM Gateway] Requisitando modelo principal: {model_preference}")
        
        result = self._try_model(prompt, system_prompt, model_preference)
        
        if not result["success"]:
            logger.warning(f"[LLM Gateway] Falha no provedor {model_preference}. Erro: {result.get('error')}")
            fallbacks = kwargs.get("fallback_models", [])
            
            if fallbacks:
                for fallback in fallbacks:
                    logger.info(f"[LLM Gateway] Tentando fallback explícito: {fallback}")
                    result = self._try_model(prompt, system_prompt, fallback)
                    if result["success"]:
                        break
                        
        if not result["success"]:
            error_msg = f"Nenhum provedor LLM real disponível ou configurado corretamente. Último erro: {result.get('error')}"
            logger.error(f"[LLM Gateway] CRÍTICO: {error_msg}")
            raise RuntimeError(error_msg)
            
        return result

    def _try_model(self, prompt: str, system_prompt: str, model: str) -> Dict[str, Any]:
        if model == "openai":
            if not self.openai_key:
                return {"success": False, "error": "OPENAI_API_KEY ausente."}
            return self._call_openai(prompt, system_prompt)
            
        elif model == "google":
            if not self.google_key:
                return {"success": False, "error": "GOOGLE_API_KEY ausente."}
            return self._call_google(prompt, system_prompt)
            
        elif model == "anthropic":
            if not self.anthropic_key:
                return {"success": False, "error": "ANTHROPIC_API_KEY ausente."}
            return self._call_anthropic(prompt, system_prompt)
            
        return {"success": False, "error": f"Provedor desconhecido: {model}"}

    def _call_openai(self, prompt: str, system_prompt: str) -> Dict[str, Any]:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_key}"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                resp_data = json.loads(response.read().decode("utf-8"))
                text = resp_data["choices"][0]["message"]["content"]
                return {"success": True, "text": text, "model": "openai-gpt-4o-mini"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _call_google(self, prompt: str, system_prompt: str) -> Dict[str, Any]:
        try:
            from a_platform.g_llm_gateway.b_providers.google.provider import GoogleProvider
            provider = GoogleProvider()
            import asyncio
            text = asyncio.run(provider.generate(prompt, system_prompt))
            return {"success": True, "text": text, "model": "google-gemini"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _call_anthropic(self, prompt: str, system_prompt: str) -> Dict[str, Any]:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.anthropic_key,
            "anthropic-version": "2023-06-01"
        }
        data = {
            "model": "claude-3-5-sonnet-20240620",
            "max_tokens": 4096,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        try:
            req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                resp_data = json.loads(response.read().decode("utf-8"))
                text = resp_data["content"][0]["text"]
                return {"success": True, "text": text, "model": "anthropic-claude-3.5"}
        except Exception as e:
            return {"success": False, "error": str(e)}
