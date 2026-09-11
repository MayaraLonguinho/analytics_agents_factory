"""
Base Workflow Manager - Interface base para gestores de workflow
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from ...interfaces import IWorkflowManager
from ...schemas import (
    WorkflowState,
    WorkflowStatus,
    AgentExecution
)


class BaseWorkflowManager(IWorkflowManager, ABC):
    """
    Classe base para gestores de workflow.
    Implementa funcionalidades comuns de gestão de workflows.
    """

    def __init__(self):
        """
        Inicializa o gestor de workflow.
        """
        self.active_workflows: Dict[str, WorkflowState] = {}
        self.completed_workflows: Dict[str, WorkflowState] = {}

    def _create_workflow_state(
        self,
        workflow_id: str,
        agent_sequence: List[str],
        input_data: Dict[str, Any]
    ) -> WorkflowState:
        """
        Cria estado inicial de workflow.

        Args:
            workflow_id: ID do workflow
            agent_sequence: Sequência de agentes
            input_data: Dados de entrada

        Returns:
            WorkflowState inicial
        """
        return WorkflowState(
            workflow_id=workflow_id,
            status=WorkflowStatus.PENDING,
            current_agent_index=0,
            agent_sequence=agent_sequence,
            accumulated_results=input_data.copy(),
            agent_executions=[],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

    def _update_agent_execution(
        self,
        state: WorkflowState,
        execution: AgentExecution
    ) -> None:
        """
        Atualiza estado com execução de agente.

        Args:
            state: Estado do workflow
            execution: Execução do agente
        """
        state.agent_executions.append(execution)

        if execution.output_data:
            state.accumulated_results.update(execution.output_data)

        state.updated_at = datetime.utcnow()

    def _advance_workflow(self, state: WorkflowState) -> None:
        """
        Avança workflow para próximo agente.

        Args:
            state: Estado do workflow
        """
        state.current_agent_index += 1
        state.updated_at = datetime.utcnow()

    def _check_workflow_completion(self, state: WorkflowState) -> bool:
        """
        Verifica se workflow está completo.

        Args:
            state: Estado do workflow

        Returns:
            True se completo, False caso contrário
        """
        return state.current_agent_index >= len(state.agent_sequence)

    def _handle_workflow_failure(
        self,
        state: WorkflowState,
        error_message: str
    ) -> None:
        """
        Trata falha de workflow.

        Args:
            state: Estado do workflow
            error_message: Mensagem de erro
        """
        state.status = WorkflowStatus.FAILED
        state.error_message = error_message
        state.updated_at = datetime.utcnow()

    def _handle_workflow_success(self, state: WorkflowState) -> None:
        """
        Trata sucesso de workflow.

        Args:
            state: Estado do workflow
        """
        state.status = WorkflowStatus.COMPLETED
        state.updated_at = datetime.utcnow()

    def _handle_workflow_cancellation(self, state: WorkflowState) -> None:
        """
        Trata cancelamento de workflow.

        Args:
            state: Estado do workflow
        """
        state.status = WorkflowStatus.CANCELLED
        state.updated_at = datetime.utcnow()

    def get_current_agent(self, state: WorkflowState) -> Optional[str]:
        """
        Retorna agente atual do workflow.

        Args:
            state: Estado do workflow

        Returns:
            Nome do agente atual ou None
        """
        if state.current_agent_index < len(state.agent_sequence):
            return state.agent_sequence[state.current_agent_index]
        return None

    def get_workflow_progress(self, state: WorkflowState) -> float:
        """
        Calcula progresso do workflow.

        Args:
            state: Estado do workflow

        Returns:
            Progresso como porcentagem (0-100)
        """
        if not state.agent_sequence:
            return 0.0

        return (state.current_agent_index / len(state.agent_sequence)) * 100

    def get_failed_agents(self, state: WorkflowState) -> List[str]:
        """
        Retorna agentes que falharam no workflow.

        Args:
            state: Estado do workflow

        Returns:
            Lista de nomes de agentes que falharam
        """
        return [
            exec.agent_name
            for exec in state.agent_executions
            if exec.status.value == "failed"
        ]

    def get_completed_agents(self, state: WorkflowState) -> List[str]:
        """
        Retorna agentes que completaram com sucesso.

        Args:
            state: Estado do workflow

        Returns:
            Lista de nomes de agentes completados
        """
        return [
            exec.agent_name
            for exec in state.agent_executions
            if exec.status.value == "completed"
        ]
