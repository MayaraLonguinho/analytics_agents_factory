"""
Interfaces de contexto do Analytics AI Factory.

Define os contratos responsáveis pelo gerenciamento do contexto
utilizado pelo Brain durante uma execução.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class IContextManager(ABC):
    """
    Interface para gerenciamento de contexto.

    O Context Manager combina informações relevantes para que
    Agents e demais componentes possam trabalhar com o contexto
    correto da execução.
    """

    @abstractmethod
    async def build_context(
        self,
        session_id: str,
        query: str,
        retrieved_docs: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """
        Constrói o contexto para uma consulta.

        Args:
            session_id: Identificador da sessão.
            query: Consulta atual.
            retrieved_docs: Documentos recuperados pelo RAG.

        Returns:
            Contexto consolidado.
        """
        pass

    @abstractmethod
    async def update_context(
        self,
        session_id: str,
        new_information: Dict[str, Any],
    ) -> bool:
        """
        Atualiza o contexto de uma sessão.

        Args:
            session_id: Identificador da sessão.
            new_information: Novas informações a adicionar.

        Returns:
            True quando o contexto foi atualizado.
        """
        pass


class IBrainManager(ABC):
    """
    Interface principal de gerenciamento do Brain.

    Define o ponto de acesso aos componentes fundamentais
    de contexto e memória.
    """

    @abstractmethod
    async def get_context_manager(self) -> IContextManager:
        """
        Recupera o gerenciador de contexto.

        Returns:
            Instância do Context Manager.
        """
        pass

    @abstractmethod
    async def get_conversation_memory(self) -> Any:
        """
        Recupera a memória de conversação.

        Returns:
            Implementação da Conversation Memory.
        """
        pass

    @abstractmethod
    async def get_long_term_memory(self) -> Any:
        """
        Recupera a memória de longo prazo.

        Returns:
            Implementação da Long Term Memory.
        """
        pass