import logging
import os
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class LLMGateway:
    """
    Gateway de LLMs com roteamento e fallback.
    Atualmente suporta fallback e telemetria mockada se não houver chaves de API.
    """
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        
    def generate_text(self, prompt: str, system_prompt: str = "", model_preference: str = "openai") -> Dict[str, Any]:
        logger.info(f"LLM Gateway invocado com preferência: {model_preference}")
        
        # Estratégia de Roteamento e Fallback
        result = self._try_model(prompt, system_prompt, model_preference)
        
        if not result["success"]:
            logger.warning(f"Falha ao usar o modelo preferido ({model_preference}). Tentando fallbacks...")
            fallbacks = [m for m in ["openai", "anthropic", "ollama"] if m != model_preference]
            
            for fallback in fallbacks:
                logger.info(f"Tentando fallback: {fallback}")
                result = self._try_model(prompt, system_prompt, fallback)
                if result["success"]:
                    break
                    
        return result

    def _try_model(self, prompt: str, system_prompt: str, model: str) -> Dict[str, Any]:
        try:
            # Aqui entraríamos com a lógica real de integração HTTP/SDK
            if model == "openai":
                if not self.openai_key:
                    return {"success": False, "error": "OPENAI_API_KEY missing", "model": model}
                # Lógica fictícia
                response_text = f"[MOCK OPENAI] Resposta para: {prompt[:50]}..."
            elif model == "anthropic":
                if not self.anthropic_key:
                    return {"success": False, "error": "ANTHROPIC_API_KEY missing", "model": model}
                # Lógica fictícia
                response_text = f"[MOCK ANTHROPIC] Resposta para: {prompt[:50]}..."
            elif model == "ollama":
                # Ollama normalmente roda localmente, assumimos sucesso no mock
                response_text = f"[MOCK OLLAMA LOCAL] Gerando código boilerplate..."
            else:
                return {"success": False, "error": f"Unknown model {model}", "model": model}
                
            return {
                "success": True,
                "text": response_text,
                "model": model,
                "usage": {"tokens": len(prompt.split()) + 50}
            }
        except Exception as e:
            return {"success": False, "error": str(e), "model": model}
