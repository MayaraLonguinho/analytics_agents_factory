"""
Orchestrator Logger - Logger especializado para o Orchestrator Agent
"""

import logging
import json
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from pathlib import Path
from threading import Lock
from ...interfaces import IExecutionLogger
from ...schemas import (
    ExecutionLog,
    AuditRecord,
    AgentExecution
)


class OrchestratorLogger(IExecutionLogger):
    """
    Implementação do logger de execução do Orchestrator.
    Responsável por registrar logs estruturados e auditoria.
    """

    def __init__(
        self,
        log_dir: str = ".orchestrator_logs",
        log_level: str = "INFO",
        enable_file_logging: bool = True,
        enable_console_logging: bool = True
    ):
        """
        Inicializa o OrchestratorLogger.

        Args:
            log_dir: Diretório para salvar logs
            log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            enable_file_logging: Habilitar logging em arquivo
            enable_console_logging: Habilitar logging no console
        """
        self.log_dir = Path(log_dir)
        self.log_level = getattr(logging, log_level.upper())
        self.enable_file_logging = enable_file_logging
        self.enable_console_logging = enable_console_logging
        self.lock = Lock()

        # Criar diretório de logs se necessário
        if enable_file_logging:
            self.log_dir.mkdir(parents=True, exist_ok=True)

        # Armazenamento de logs em memória
        self.logs: Dict[str, List[ExecutionLog]] = {}
        self.audit_records: List[AuditRecord] = []

        # Configurar logger do Python
        self._setup_python_logger()

    def _setup_python_logger(self) -> None:
        """Configura o logger do Python."""
        self.logger = logging.getLogger("orchestrator")
        self.logger.setLevel(self.log_level)

        # Remover handlers existentes
        self.logger.handlers.clear()

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Console handler
        if self.enable_console_logging:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.log_level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        # File handler
        if self.enable_file_logging:
            log_file = self.log_dir / "orchestrator.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(self.log_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def _create_execution_log(
        self,
        workflow_id: str,
        level: str,
        event_type: str,
        message: str,
        agent_name: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> ExecutionLog:
        """
        Cria um registro de log de execução.

        Args:
            workflow_id: ID do workflow
            level: Nível de log
            event_type: Tipo de evento
            message: Mensagem do log
            agent_name: Nome do agente (opcional)
            data: Dados adicionais (opcional)

        Returns:
            ExecutionLog criado
        """
        import uuid

        return ExecutionLog(
            log_id=str(uuid.uuid4()),
            workflow_id=workflow_id,
            timestamp=datetime.utcnow(),
            level=level,
            event_type=event_type,
            agent_name=agent_name,
            message=message,
            data=data
        )

    def _store_log(self, log: ExecutionLog) -> None:
        """
        Armazena um log na memória.

        Args:
            log: Log a armazenar
        """
        with self.lock:
            if log.workflow_id not in self.logs:
                self.logs[log.workflow_id] = []

            self.logs[log.workflow_id].append(log)

            # Log usando Python logger
            log_level = getattr(logging, log.level.upper(), logging.INFO)
            self.logger.log(
                log_level,
                f"[{log.workflow_id}] {log.event_type}: {log.message}"
            )

            # Salvar em arquivo se habilitado
            if self.enable_file_logging:
                self._save_log_to_file(log)

    def _save_log_to_file(self, log: ExecutionLog) -> None:
        """
        Salva log em arquivo JSON específico do workflow.

        Args:
            log: Log a salvar
        """
        log_file = self.log_dir / f"{log.workflow_id}.jsonl"

        with open(log_file, 'a') as f:
            f.write(json.dumps(log.dict(), default=str) + '\n')

    def log_workflow_start(
        self,
        workflow_id: str,
        input_data: Union[Dict[str, Any], object]
    ) -> None:
        """
        Registra início de workflow.

        Args:
            workflow_id: ID do workflow
            input_data: Dados de entrada
        """
        # Extrair dados do input
        if hasattr(input_data, 'dict'):
            input_dict = input_data.dict()
            requirements = input_dict.get('requirements', '')
            project_name = input_dict.get('project_name', '')
            priority = input_dict.get('priority', 'normal')
        else:
            input_dict = input_data if isinstance(input_data, dict) else {}
            requirements = input_dict.get('requirements', '')
            project_name = input_dict.get('project_name', '')
            priority = input_dict.get('priority', 'normal')

        log = self._create_execution_log(
            workflow_id=workflow_id,
            level="INFO",
            event_type="workflow_start",
            message=f"Workflow started: {workflow_id}",
            data={
                "requirements": requirements[:100] + "..." if len(requirements) > 100 else requirements,
                "project_name": project_name,
                "priority": priority
            }
        )

        self._store_log(log)

        # Criar registro de auditoria
        self._create_audit_record(
            workflow_id=workflow_id,
            action="workflow_start",
            actor="orchestrator",
            details={"input_data": input_dict}
        )

    def log_workflow_end(
        self,
        workflow_id: str,
        output_data: Union[Dict[str, Any], object]
    ) -> None:
        """
        Registra fim de workflow.

        Args:
            workflow_id: ID do workflow
            output_data: Dados de saída
        """
        # Extrair dados do output
        if hasattr(output_data, 'dict'):
            output_dict = output_data.dict()
            status = output_dict.get('status', 'unknown')
            execution_time = output_dict.get('execution_time', 0.0)
            agent_executions = output_dict.get('agent_executions', [])
        else:
            output_dict = output_data if isinstance(output_data, dict) else {}
            status = output_dict.get('status', 'unknown')
            execution_time = output_dict.get('execution_time', 0.0)
            agent_executions = output_dict.get('agent_executions', [])

        log = self._create_execution_log(
            workflow_id=workflow_id,
            level="INFO",
            event_type="workflow_end",
            message=f"Workflow completed: {workflow_id} with status {status}",
            data={
                "status": status.value if hasattr(status, 'value') else status,
                "execution_time": execution_time,
                "total_agents": len(agent_executions),
                "successful_agents": sum(
                    1 for e in agent_executions
                    if e.get('status') == 'completed' or (hasattr(e, 'status') and e.status.value == 'completed')
                ),
                "failed_agents": sum(
                    1 for e in agent_executions
                    if e.get('status') == 'failed' or (hasattr(e, 'status') and e.status.value == 'failed')
                )
            }
        )

        self._store_log(log)

        # Criar registro de auditoria
        self._create_audit_record(
            workflow_id=workflow_id,
            action="workflow_end",
            actor="orchestrator",
            details={"output_data": output_dict}
        )

    def log_agent_start(
        self,
        workflow_id: str,
        agent_name: str,
        input_data: Dict[str, Any]
    ) -> None:
        """
        Registra início de execução de agente.

        Args:
            workflow_id: ID do workflow
            agent_name: Nome do agente
            input_data: Dados de entrada
        """
        log = self._create_execution_log(
            workflow_id=workflow_id,
            level="INFO",
            event_type="agent_start",
            message=f"Agent {agent_name} started",
            agent_name=agent_name,
            data={
                "input_keys": list(input_data.keys()) if input_data else []
            }
        )

        self._store_log(log)

    def log_agent_end(
        self,
        workflow_id: str,
        agent_name: str,
        execution: Union[AgentExecution, Dict[str, Any]]
    ) -> None:
        """
        Registra fim de execução de agente.

        Args:
            workflow_id: ID do workflow
            agent_name: Nome do agente
            execution: Dados da execução
        """
        # Extrair dados da execução
        if hasattr(execution, 'dict'):
            exec_dict = execution.dict()
            status = exec_dict.get('status', 'unknown')
            execution_time = exec_dict.get('execution_time', 0.0)
            retry_count = exec_dict.get('retry_count', 0)
            output_data = exec_dict.get('output_data')
            error_message = exec_dict.get('error_message')
        else:
            exec_dict = execution if isinstance(execution, dict) else {}
            status = exec_dict.get('status', 'unknown')
            execution_time = exec_dict.get('execution_time', 0.0)
            retry_count = exec_dict.get('retry_count', 0)
            output_data = exec_dict.get('output_data')
            error_message = exec_dict.get('error_message')

        # Determinar nível de log
        status_value = status.value if hasattr(status, 'value') else status
        level = "INFO" if status_value == "completed" else "ERROR"

        log = self._create_execution_log(
            workflow_id=workflow_id,
            level=level,
            event_type="agent_end",
            message=f"Agent {agent_name} {status_value}",
            agent_name=agent_name,
            data={
                "status": status_value,
                "execution_time": execution_time,
                "retry_count": retry_count,
                "has_output": output_data is not None,
                "error": error_message
            }
        )

        self._store_log(log)

    def log_error(
        self,
        workflow_id: str,
        agent_name: Optional[str],
        error: Exception,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Registra erro durante execução.

        Args:
            workflow_id: ID do workflow
            agent_name: Nome do agente (opcional)
            error: Exceção ocorrida
            context: Contexto adicional
        """
        log = self._create_execution_log(
            workflow_id=workflow_id,
            level="ERROR",
            event_type="error",
            message=f"Error: {type(error).__name__}: {str(error)}",
            agent_name=agent_name,
            data={
                "error_type": type(error).__name__,
                "error_message": str(error),
                "context": context
            }
        )

        self._store_log(log)

        # Criar registro de auditoria para erros
        self._create_audit_record(
            workflow_id=workflow_id,
            action="error",
            actor=agent_name or "orchestrator",
            details={
                "error_type": type(error).__name__,
                "error_message": str(error),
                "context": context
            }
        )

    def get_workflow_logs(self, workflow_id: str) -> List[Dict[str, Any]]:
        """
        Recupera logs de um workflow.

        Args:
            workflow_id: ID do workflow

        Returns:
            Lista de logs do workflow
        """
        with self.lock:
            if workflow_id not in self.logs:
                return []

            return [log.dict() for log in self.logs[workflow_id]]

    def get_logs_by_level(
        self,
        workflow_id: str,
        level: str
    ) -> List[Dict[str, Any]]:
        """
        Recupera logs de um workflow filtrados por nível.

        Args:
            workflow_id: ID do workflow
            level: Nível de log

        Returns:
            Lista de logs filtrados
        """
        with self.lock:
            if workflow_id not in self.logs:
                return []

            return [
                log.dict()
                for log in self.logs[workflow_id]
                if log.level == level
            ]

    def get_logs_by_event_type(
        self,
        workflow_id: str,
        event_type: str
    ) -> List[Dict[str, Any]]:
        """
        Recupera logs de um workflow filtrados por tipo de evento.

        Args:
            workflow_id: ID do workflow
            event_type: Tipo de evento

        Returns:
            Lista de logs filtrados
        """
        with self.lock:
            if workflow_id not in self.logs:
                return []

            return [
                log.dict()
                for log in self.logs[workflow_id]
                if log.event_type == event_type
            ]

    def get_logs_by_agent(
        self,
        workflow_id: str,
        agent_name: str
    ) -> List[Dict[str, Any]]:
        """
        Recupera logs de um workflow filtrados por agente.

        Args:
            workflow_id: ID do workflow
            agent_name: Nome do agente

        Returns:
            Lista de logs filtrados
        """
        with self.lock:
            if workflow_id not in self.logs:
                return []

            return [
                log.dict()
                for log in self.logs[workflow_id]
                if log.agent_name == agent_name
            ]

    def _create_audit_record(
        self,
        workflow_id: str,
        action: str,
        actor: str,
        target: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Cria um registro de auditoria.

        Args:
            workflow_id: ID do workflow
            action: Ação realizada
            actor: Entidade que realizou a ação
            target: Alvo da ação (opcional)
            details: Detalhes da ação (opcional)
        """
        import uuid

        audit_record = AuditRecord(
            audit_id=str(uuid.uuid4()),
            workflow_id=workflow_id,
            timestamp=datetime.utcnow(),
            action=action,
            actor=actor,
            target=target,
            details=details or {}
        )

        with self.lock:
            self.audit_records.append(audit_record)

            # Salvar em arquivo se habilitado
            if self.enable_file_logging:
                audit_file = self.log_dir / "audit.jsonl"
                with open(audit_file, 'a') as f:
                    f.write(json.dumps(audit_record.dict(), default=str) + '\n')

    def get_audit_records(
        self,
        workflow_id: Optional[str] = None,
        action: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Recupera registros de auditoria.

        Args:
            workflow_id: Filtrar por workflow (opcional)
            action: Filtrar por ação (opcional)
            limit: Limite de registros

        Returns:
            Lista de registros de auditoria
        """
        with self.lock:
            records = self.audit_records

            if workflow_id:
                records = [r for r in records if r.workflow_id == workflow_id]

            if action:
                records = [r for r in records if r.action == action]

            # Retornar os mais recentes
            records = sorted(records, key=lambda x: x.timestamp, reverse=True)

            return [r.dict() for r in records[:limit]]

    def clear_workflow_logs(self, workflow_id: str) -> None:
        """
        Limpa logs de um workflow específico.

        Args:
            workflow_id: ID do workflow
        """
        with self.lock:
            if workflow_id in self.logs:
                del self.logs[workflow_id]

            # Remover arquivo de logs se existir
            if self.enable_file_logging:
                log_file = self.log_dir / f"{workflow_id}.jsonl"
                if log_file.exists():
                    log_file.unlink()

    def clear_old_logs(self, days: int = 30) -> int:
        """
        Limpa logs antigos.

        Args:
            days: Número de dias para manter

        Returns:
            Número de logs removidos
        """
        from datetime import timedelta

        with self.lock:
            cutoff = datetime.utcnow() - timedelta(days=days)
            removed = 0

            # Limpar logs na memória
            for workflow_id in list(self.logs.keys()):
                workflow_logs = self.logs[workflow_id]
                self.logs[workflow_id] = [
                    log for log in workflow_logs
                    if log.timestamp >= cutoff
                ]

                removed += len(workflow_logs) - len(self.logs[workflow_id])

                # Limpar workflows sem logs
                if not self.logs[workflow_id]:
                    del self.logs[workflow_id]

            # Limpar registros de auditoria
            self.audit_records = [
                record for record in self.audit_records
                if record.timestamp >= cutoff
            ]

            # Limpar arquivos antigos
            if self.enable_file_logging:
                for log_file in self.log_dir.glob("*.jsonl"):
                    if log_file.stat().st_mtime < cutoff.timestamp():
                        log_file.unlink()
                        removed += 1

            return removed

    def get_log_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas de logs.

        Returns:
            Dicionário com estatísticas
        """
        with self.lock:
            total_logs = sum(len(logs) for logs in self.logs.values())
            total_workflows = len(self.logs)
            total_audit_records = len(self.audit_records)

            # Contar logs por nível
            level_counts = {}
            for workflow_logs in self.logs.values():
                for log in workflow_logs:
                    level_counts[log.level] = level_counts.get(log.level, 0) + 1

            # Contar logs por tipo de evento
            event_counts = {}
            for workflow_logs in self.logs.values():
                for log in workflow_logs:
                    event_counts[log.event_type] = event_counts.get(log.event_type, 0) + 1

            return {
                "total_logs": total_logs,
                "total_workflows": total_workflows,
                "total_audit_records": total_audit_records,
                "logs_by_level": level_counts,
                "logs_by_event_type": event_counts
            }
