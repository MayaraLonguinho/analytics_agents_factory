"""
LLM Gateway - OpenAI Provider
Provider específico para OpenAI
"""

from typing import Dict, Any, Optional, AsyncGenerator
from ...f_interfaces.a_base_provider import BaseLLMProvider, LLMRequest, LLMResponse


class OpenAIProvider(BaseLLMProvider):
    """
    Provider específico para OpenAI.
    
    Implementa a interface base para comunicação com os modelos da OpenAI.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa o Provider OpenAI.
        
        Args:
            config: Configuração do Provider
        """
        super().__init__(config)
        self._client = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Inicializa o cliente OpenAI"""
        try:
            from openai import AsyncOpenAI
            
            api_key = self.config.get("api_key")
            base_url = self.config.get("base_url")
            
            self._client = AsyncOpenAI(
                api_key=api_key,
                base_url=base_url
            )
                
        except ImportError:
            raise ImportError(
                "OpenAI não está instalado. "
                "Instale com: pip install openai"
            )
    
    async def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Gera uma resposta não-streaming.
        
        Args:
            request: Requisição LLM
            
        Returns:
            LLMResponse: Resposta do modelo
        """
        try:
            parameters = request.parameters or {}
            
            response = await self._client.chat.completions.create(
                model=request.model,
                messages=[{"role": "user", "content": request.prompt}],
                max_tokens=request.max_tokens or parameters.get("max_tokens"),
                temperature=request.temperature or parameters.get("temperature", 0.7),
                **{k: v for k, v in parameters.items() 
                   if k not in ["max_tokens", "temperature"]}
            )
            
            return LLMResponse(
                content=response.choices[0].message.content,
                model=request.model,
                provider="openai",
                tokens_used=response.usage.total_tokens,
                finish_reason=response.choices[0].finish_reason,
                metadata={"id": response.id}
            )
            
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar resposta com OpenAI: {e}")
    
    async def chat(self, messages: list, model: str, **kwargs) -> LLMResponse:
        """
        Gera uma resposta de chat.
        
        Args:
            messages: Lista de mensagens do chat
            model: Nome do modelo
            **kwargs: Parâmetros adicionais
            
        Returns:
            LLMResponse: Resposta do modelo
        """
        try:
            response = await self._client.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs
            )
            
            return LLMResponse(
                content=response.choices[0].message.content,
                model=model,
                provider="openai",
                tokens_used=response.usage.total_tokens,
                finish_reason=response.choices[0].finish_reason
            )
            
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar chat com OpenAI: {e}")
    
    async def embeddings(self, text: str, model: str, **kwargs) -> list:
        """
        Gera embeddings para um texto.
        
        Args:
            text: Texto para gerar embeddings
            model: Nome do modelo
            **kwargs: Parâmetros adicionais
            
        Returns:
            list: Vetor de embeddings
        """
        try:
            response = await self._client.embeddings.create(
                model=model,
                input=text,
                **kwargs
            )
            
            return response.data[0].embedding
            
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar embeddings com OpenAI: {e}")
    
    async def stream(self, request: LLMRequest) -> AsyncGenerator[str, None]:
        """
        Gera uma resposta streaming.
        
        Args:
            request: Requisição LLM
            
        Yields:
            str: Chunks da resposta
        """
        try:
            parameters = request.parameters or {}
            
            stream = await self._client.chat.completions.create(
                model=request.model,
                messages=[{"role": "user", "content": request.prompt}],
                max_tokens=request.max_tokens or parameters.get("max_tokens"),
                temperature=request.temperature or parameters.get("temperature", 0.7),
                stream=True,
                **{k: v for k, v in parameters.items() 
                   if k not in ["max_tokens", "temperature"]}
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            raise RuntimeError(f"Erro ao gerar stream com OpenAI: {e}")
    
    async def health_check(self) -> bool:
        """
        Verifica se o Provider está saudável.
        
        Returns:
            bool: True se saudável, False caso contrário
        """
        try:
            response = await self._client.chat.completions.create(
                model=self.config.get("default_model", "gpt-3.5-turbo"),
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=5
            )
            return True
        except Exception:
            return False
