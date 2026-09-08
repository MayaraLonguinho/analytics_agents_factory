"""
Execution History - Histórico de execuções
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from threading import Lock
from ...interfaces import IExecutionHistory
from ...schemas import AgentExecution, AgentExecutionStatus


class ExecutionHistory(IExecutionHistory):
    """
    Implementação do histórico de execuções.
    Responsável por manter registro completo de execuções.
    """

    def __init__(self, max_history_size: int = 10000):
        """
        Inicializa o histórico de execuções.

        Args:
            max_history_size: Tamanho máximo do histórico
        """
        self.max_history_size = max_history_size
        self.workflow_history: Dict[str, List[AgentExecution]] = defaultdict(list)
        self.agent_history: Dict[str, List[AgentExecution]] = defaultdict(list)
        self.all_executions: List[AgentExecution] = []
        self.lock = Lock()

    def record_execution(
        self,
        workflow_id: str,
        execution: AgentExecution
    ) -> None:
        """
        Registra uma execução de agente.

        Args:
            workflow_id: ID do workflow
            execution: Dados da execução
        """
        with self.lock:
            # Adicionar ao histórico do workflow
            self.workflow_history[workflow_id].append(execution)

            # Adicionar ao histórico do agente
            self.agent_history[execution.agent_name].append(execution)

            # Adicionar ao histórico geral
            self.all_executions.append(execution)

            # Limpar se exceder tamanho máximo
            if len(self.all_executions) > self.max_history_size:
                self._cleanup_old_executions()

    def get_workflow_history(self, workflow_id: str) -> List[AgentExecution]:
        """
        Recupera histórico de execuções de um workflow.

        Args:
            workflow_id: ID do workflow

        Returns:
            Lista de execuções do workflow
        """
        with self.lock:
            return self.workflow_history.get(workflow_id, []).copy()

    def get_agent_history(
        self,
        agent_name: str,
        limit: int = 100
    ) -> List[AgentExecution]:
        """
        Recupera histórico de execuções de um agente.

        Args:
            agent_name: Nome do agente
            limit: Limite de registros

        Returns:
            Lista de execuções do agente
        """
        with self.lock:
            history = self.agent_history.get(agent_name, [])
            # Retornar as mais recentes
            return sorted(history, key=lambda x: x.timestamp, reverse=True)[:limit]

    def get_execution_statistics(
        self,
        workflow_id: Optional[str] = None,
        agent_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Recupera estatísticas de execução.

        Args:
            workflow_id: ID do workflow (opcional)
            agent_name: Nome do agente (opcional)

        Returns:
            Dicionário com estatísticas
        """
        with self.lock:
            # Filtrar execuções baseado nos parâmetros
            executions = self._filter_executions(workflow_id, agent_name)

            if not executions:
                return {
                    "total_executions": 0,
                    "successful": 0,
                    "failed": 0,
                    "skipped": 0,
                    "average_execution_time": 0.0,
                    "success_rate": 0.0
                }

            # Calcular estatísticas básicas
            total = len(executions)
            successful = sum(
                1 for e in executions
                if e.status == AgentExecutionStatus.COMPLETED
            )
            failed = sum(
                1 for e in executions
                if e.status == AgentExecutionStatus.FAILED
            )
            skipped = sum(
                1 for e in executions
                if e.status == AgentExecutionStatus.SKIPPED
            )

            # Calcular tempo médio de execução
            execution_times = [e.execution_time for e in executions if e.execution_time > 0]
            avg_time = sum(execution_times) / len(execution_times) if execution_times else 0.0

            # Calcular taxa de sucesso
            success_rate = successful / total if total > 0 else 0.0

            # Calcular estatísticas por agente se não filtrado por agente
            agent_stats = {}
            if not agent_name:
                agent_names = set(e.agent_name for e in executions)
                for name in agent_names:
                    agent_execs = [e for e in executions if e.agent_name == name]
                    agent_successful = sum(
                        1 for e in agent_execs
                        if e.status == AgentExecutionStatus.COMPLETED
                    )
                    agent_stats[name] = {
                        "total": len(agent_execs),
                        "successful": agent_successful,
                        "success_rate": agent_successful / len(agent_execs) if agent_execs else 0.0
                    }

            return {
                "total_executions": total,
                "successful": successful,
                "failed": failed,
                "skipped": skipped,
                "average_execution_time": avg_time,
                "success_rate": success_rate,
                "agent_statistics": agent_stats
            }

    def get_recent_executions(
        self,
        limit: int = 50,
        agent_name: Optional[str] = None
    ) -> List[AgentExecution]:
        """
        Recupera execuções recentes.

        Args:
            limit: Limite de registros
            agent_name: Filtrar por agente (opcional)

        Returns:
            Lista de execuções recentes
        """
        with self.lock:
            executions = self.all_executions

            if agent_name:
                executions = [e for e in executions if e.agent_name == agent_name]

            # Ordenar por timestamp (mais recentes primeiro)
            return sorted(executions, key=lambda x: x.timestamp, reverse=True)[:limit]

    def get_failed_executions(
        self,
        limit: int = 50,
        agent_name: Optional[str] = None
    ) -> List[AgentExecution]:
        """
        Recupera execuções que falharam.

        Args:
            limit: Limite de registros
            agent_name: Filtrar por agente (opcional)

        Returns:
            Lista de execuções falhas
        """
        with self.lock:
            executions = [
                e for e in self.all_executions
                if e.status == AgentExecutionStatus.FAILED
            ]

            if agent_name:
                executions = [e for e in executions if e.agent_name == agent_name]

            return sorted(executions, key=lambda x: x.timestamp, reverse=True)[:limit]

    def get_execution_by_id(
        self,
        execution_id: str
    ) -> Optional[AgentExecution]:
        """
        Recupera execução por ID (timestamp + agent_name).

        Args:
            execution_id: ID da execução

        Returns:
            Execução ou None
        """
        with self.lock:
            for execution in self.all_executions:
                # Criar ID composto
                exec_id = f"{execution.agent_name}_{execution.timestamp.isoformat()}"
                if exec_id == execution_id:
                    return execution

            return None

    def get_executions_in_period(
        self,
        start_date: datetime,
        end_date: datetime,
        agent_name: Optional[str] = None
    ) -> List[AgentExecution]:
        """
        Recupera execuções em um período de tempo.

        Args:
            start_date: Data inicial
            end_date: Data final
            agent_name: Filtrar por agente (opcional)

        Returns:
            Lista de execuções no período
        """
        with self.lock:
            executions = [
                e for e in self.all_executions
                if start_date <= e.timestamp <= end_date
            ]

            if agent_name:
                executions = [e for e in executions if e.agent_name == agent_name]

            return sorted(executions, key=lambda x: x.timestamp)

    def clear_workflow_history(self, workflow_id: str) -> int:
        """
        Limpa histórico de um workflow específico.

        Args:
            workflow_id: ID do workflow

        Returns:
            Número de execuções removidas
        """
        with self.lock:
            if workflow_id not in self.workflow_history:
                return 0

            removed_count = len(self.workflow_history[workflow_id])

            # Remover do histórico do workflow
            del self.workflow_history[workflow_id]

            # Remover execuções do histórico geral
            self.all_executions = [
                e for e in self.all_executions
                if not self._is_execution_in_workflow(e, workflow_id)
            ]

            # Remover do histórico de agentes
            for agent_name in list(self.agent_history.keys()):
                self.agent_history[agent_name] = [
                    e for e in self.agent_history[agent_name]
                    if not self._is_execution_in_workflow(e, workflow_id)
                ]

                # Limpar entradas vazias
                if not self.agent_history[agent_name]:
                    del self.agent_history[agent_name]

            return removed_count

    def clear_old_executions(self, days: int = 30) -> int:
        """
        Limpa execuções antigas.

        Args:
            days: Número de dias para manter

        Returns:
            Número de execuções removidas
        """
        with self.lock:
            cutoff = datetime.utcnow() - timedelta(days=days)
            old_count = len(self.all_executions)

            # Filtrar execuções recentes
            self.all_executions = [
                e for e in self.all_executions
                if e.timestamp >= cutoff
            ]

            # Atualizar históricos por workflow
            for workflow_id in list(self.workflow_history.keys()):
                self.workflow_history[workflow_id] = [
                    e for e in self.workflow_history[workflow_id]
                    if e.timestamp >= cutoff
                ]

                # Limpar entradas vazias
                if not self.workflow_history[workflow_id]:
                    del self.workflow_history[workflow_id]

            # Atualizar históricos por agente
            for agent_name in list(self.agent_history.keys()):
                self.agent_history[agent_name] = [
                    e for e in self.agent_history[agent_name]
                    if e.timestamp >= cutoff
                ]

                # Limpar entradas vazias
                if not self.agent_history[agent_name]:
                    del self.agent_history[agent_name]

            return old_count - len(self.all_executions)

    def get_error_summary(
        self,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Resume erros de execução.

        Args:
            limit: Limite de erros a resumir

        Returns:
            Dicionário com resumo de erros
        """
        with self.lock:
            failed_executions = self.get_failed_executions(limit)

            # Agrupar por tipo de erro
            error_types = defaultdict(int)
            error_messages = defaultdict(int)

            for execution in failed_executions:
                if execution.error_message:
                    # Extrair tipo do erro da mensagem
                    error_type = execution.error_message.split(':')[0] if ':' in execution.error_message else 'Unknown'
                    error_types[error_type] += 1
                    error_messages[execution.error_message] += 1

            # Agrupar por agente
            agent_errors = defaultdict(int)
            for execution in failed_executions:
                agent_errors[execution.agent_name] += 1

            return {
                "total_failed": len(failed_executions),
                "error_types": dict(error_types),
                "most_common_errors": dict(sorted(error_messages.items(), key=lambda x: x[1], reverse=True)[:5]),
                "agents_with_most_errors": dict(sorted(agent_errors.items(), key=lambda x: x[1], reverse=True)[:5])
            }

    def _filter_executions(
        self,
        workflow_id: Optional[str],
        agent_name: Optional[str]
    ) -> List[AgentExecution]:
        """
        Filtra execuções baseado em parâmetros.

        Args:
            workflow_id: ID do workflow
            agent_name: Nome do agente

        Returns:
            Lista de execuções filtradas
        """
        executions = self.all_executions

        if workflow_id:
            executions = [
                e for e in executions
                if self._is_execution_in_workflow(e, workflow_id)
            ]

        if agent_name:
            executions = [e for e in executions if e.agent_name == agent_name]

        return executions

    def _is_execution_in_workflow(
        self,
        execution: AgentExecution,
        workflow_id: str
    ) -> bool:
        """
        Verifica se execução pertence a um workflow.

        Args:
            execution: Execução a verificar
            workflow_id: ID do workflow

        Returns:
            True se pertence, False caso contrário
        """
        return workflow_id in self.workflow_history and execution in self.workflow_history[workflow_id]

    def _cleanup_old_executions(self) -> None:
        """
        Remove execuções mais antigas para manter tamanho máximo.
        """
        # Ordenar por timestamp e remover as mais antigas
        self.all_executions = sorted(self.all_executions, key=lambda x: x.timestamp)[-self.max_history_size:]

        # Atualizar índices
        self.workflow_history.clear()
        self.agent_history.clear()

        for execution in self.all_executions:
            # Reconstituir índices
            workflow_id = getattr(execution, 'workflow_id', 'unknown')
            self.workflow_history[workflow_id].append(execution)
            self.agent_history[execution.agent_name].append(execution)
