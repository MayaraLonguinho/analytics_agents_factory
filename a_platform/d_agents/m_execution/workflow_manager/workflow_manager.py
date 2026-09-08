"""
Workflow Manager - Implementação do gestor de workflow
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from .base_workflow import BaseWorkflowManager
from ...schemas import (
    WorkflowState,
    WorkflowStatus,
    AgentExecution,
    ExecutionPlan,
    WorkflowConfig
)
from ...interfaces import IStateManager, IExecutionLogger
from ...utils import calculate_execution_time


class WorkflowManager(BaseWorkflowManager):
    """
    Implementação do gestor de workflow.
    Responsável por gerenciar ciclo de vida de workflows.
    """

    def __init__(
        self,
        state_manager: Optional[IStateManager] = None,
        logger: Optional[IExecutionLogger] = None
    ):
        """
        Inicializa o WorkflowManager.

        Args:
            state_manager: Gerenciador de estado opcional
            logger: Logger de execução opcional
        """
        super().__init__()
        self.state_manager = state_manager
        self.logger = logger

    async def create_workflow(
        self,
        workflow_id: str,
        agent_sequence: List[str],
        input_data: Dict[str, Any]
    ) -> None:
        """
        Cria um novo workflow.

        Args:
            workflow_id: Identificador único do workflow
            agent_sequence: Sequência de agentes a executar
            input_data: Dados iniciais
        """
        state = self._create_workflow_state(
            workflow_id,
            agent_sequence,
            input_data
        )

        self.active_workflows[workflow_id] = state

        # Persistir estado se state manager disponível
        if self.state_manager:
            self.state_manager.save_state(workflow_id, state.dict())

        # Log criação se logger disponível
        if self.logger:
            self.logger.log_workflow_start(workflow_id, input_data)

    async def update_workflow_status(
        self,
        workflow_id: str,
        status: str,
        agent_name: Optional[str] = None,
        result: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Atualiza o status de um workflow.

        Args:
            workflow_id: Identificador do workflow
            status: Novo status
            agent_name: Nome do agente atual (opcional)
            result: Resultado parcial (opcional)
        """
        if workflow_id not in self.active_workflows:
            raise ValueError(f"Workflow {workflow_id} not found")

        state = self.active_workflows[workflow_id]
        state.status = WorkflowStatus(status)
        state.updated_at = datetime.utcnow()

        if result:
            state.accumulated_results.update(result)

        # Persistir estado se state manager disponível
        if self.state_manager:
            self.state_manager.save_state(workflow_id, state.dict())

    def get_workflow_state(self, workflow_id: str) -> Dict[str, Any]:
        """
        Recupera o estado completo de um workflow.

        Args:
            workflow_id: Identificador do workflow

        Returns:
            Dicionário com estado completo do workflow
        """
        # Tentar recuperar da memória
        if workflow_id in self.active_workflows:
            return self.active_workflows[workflow_id].dict()

        # Tentar recuperar de workflows completados
        if workflow_id in self.completed_workflows:
            return self.completed_workflows[workflow_id].dict()

        # Tentar recuperar do state manager
        if self.state_manager:
            saved_state = self.state_manager.load_state(workflow_id)
            if saved_state:
                return saved_state

        raise ValueError(f"Workflow {workflow_id} not found")

    async def execute_workflow(
        self,
        plan: ExecutionPlan,
        dispatcher,
        execution_context
    ) -> Dict[str, Any]:
        """
        Executa um workflow completo baseado em um plano.

        Args:
            plan: Plano de execução
            dispatcher: Dispatcher de agentes
            execution_context: Contexto de execução

        Returns:
            Dicionário com resultado do workflow
        """
        workflow_id = plan.workflow_id
        agent_sequence = plan.agent_sequence
        dependencies = plan.dependencies
        config = plan.config

        # Criar workflow
        await self.create_workflow(
            workflow_id,
            agent_sequence,
            {}
        )

        # Criar contexto de execução
        execution_context.create_context(workflow_id, {"plan": plan.dict()})

        start_time = datetime.utcnow()

        try:
            # Atualizar status para running
            await self.update_workflow_status(workflow_id, WorkflowStatus.RUNNING)

            # Preparar tarefas de agentes
            agent_tasks = [
                {
                    "agent_name": agent,
                    "input_data": {},
                    "config": None
                }
                for agent in agent_sequence
            ]

            # Executar com dependências
            if dependencies:
                executions = await dispatcher.dispatch_with_dependencies(
                    agent_tasks,
                    dependencies,
                    config
                )
            else:
                executions = await dispatcher.dispatch_sequence(
                    agent_tasks,
                    config
                )

            # Atualizar estado com execuções
            state = self.active_workflows[workflow_id]
            for execution in executions:
                self._update_agent_execution(state, execution)

                # Log execução se logger disponível
                if self.logger:
                    self.logger.log_agent_end(workflow_id, execution.agent_name, execution)

                # Atualizar contexto
                if execution.status.value == "completed" and execution.output_data:
                    execution_context.merge_results(
                        workflow_id,
                        execution.agent_name,
                        execution.output_data
                    )

            # Verificar se houve falhas
            failed_agents = self.get_failed_agents(state)
            if failed_agents and not config.continue_on_error:
                self._handle_workflow_failure(
                    state,
                    f"Agents failed: {', '.join(failed_agents)}"
                )
            else:
                self._handle_workflow_success(state)

            # Mover para completados
            self.completed_workflows[workflow_id] = state
            del self.active_workflows[workflow_id]

            # Limpar contexto
            execution_context.delete_context(workflow_id)

            # Log fim do workflow
            if self.logger:
                end_time = datetime.utcnow()
                execution_time = calculate_execution_time(start_time, end_time)
                self.logger.log_workflow_end(
                    workflow_id,
                    {
                        "workflow_id": workflow_id,
                        "status": state.status.value,
                        "results": state.accumulated_results,
                        "execution_time": execution_time,
                        "agent_executions": [e.dict() for e in state.agent_executions]
                    }
                )

            return state.dict()

        except Exception as e:
            # Tratar erro inesperado
            state = self.active_workflows.get(workflow_id)
            if state:
                self._handle_workflow_failure(state, str(e))

                # Mover para completados
                self.completed_workflows[workflow_id] = state
                del self.active_workflows[workflow_id]

            # Log erro
            if self.logger:
                self.logger.log_error(workflow_id, None, e)

            raise

    async def cancel_workflow(self, workflow_id: str) -> bool:
        """
        Cancela a execução de um workflow.

        Args:
            workflow_id: Identificador único do workflow

        Returns:
            True se cancelado com sucesso, False caso contrário
        """
        if workflow_id not in self.active_workflows:
            return False

        state = self.active_workflows[workflow_id]
        self._handle_workflow_cancellation(state)

        # Mover para completados
        self.completed_workflows[workflow_id] = state
        del self.active_workflows[workflow_id]

        # Persistir estado
        if self.state_manager:
            self.state_manager.save_state(workflow_id, state.dict())

        # Log cancelamento
        if self.logger:
            self.logger.log_error(
                workflow_id,
                None,
                Exception("Workflow cancelled by user"),
                {"action": "cancel"}
            )

        return True

    def list_active_workflows(self) -> List[str]:
        """
        Lista workflows ativos.

        Returns:
            Lista de IDs de workflows ativos
        """
        return list(self.active_workflows.keys())

    def list_completed_workflows(self) -> List[str]:
        """
        Lista workflows completados.

        Returns:
            Lista de IDs de workflows completados
        """
        return list(self.completed_workflows.keys())

    def get_workflow_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas de workflows.

        Returns:
            Dicionário com estatísticas
        """
        total_active = len(self.active_workflows)
        total_completed = len(self.completed_workflows)

        successful = sum(
            1 for state in self.completed_workflows.values()
            if state.status == WorkflowStatus.COMPLETED
        )

        failed = sum(
            1 for state in self.completed_workflows.values()
            if state.status == WorkflowStatus.FAILED
        )

        cancelled = sum(
            1 for state in self.completed_workflows.values()
            if state.status == WorkflowStatus.CANCELLED
        )

        return {
            "total_active": total_active,
            "total_completed": total_completed,
            "successful": successful,
            "failed": failed,
            "cancelled": cancelled,
            "success_rate": successful / total_completed if total_completed > 0 else 0.0
        }
