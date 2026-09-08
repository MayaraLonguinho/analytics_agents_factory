"""
Utils do Orchestrator Agent
Funções auxiliares para operações comuns
"""

import uuid
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta


def generate_workflow_id() -> str:
    """
    Gera um identificador único para workflow.
    
    Returns:
        String UUID única
    """
    return str(uuid.uuid4())


def calculate_execution_time(start_time: datetime, end_time: datetime) -> float:
    """
    Calcula o tempo de execução em segundos.
    
    Args:
        start_time: Timestamp de início
        end_time: Timestamp de fim
        
    Returns:
        Tempo de execução em segundos
    """
    return (end_time - start_time).total_seconds()


def format_execution_time(seconds: float) -> str:
    """
    Formata tempo de execução para string legível.
    
    Args:
        seconds: Tempo em segundos
        
    Returns:
        String formatada (ex: "1h 30m 45s")
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def should_retry(
    retry_count: int, 
    max_retries: int, 
    error: Exception
) -> bool:
    """
    Determina se deve tentar novamente baseado no erro e número de tentativas.
    
    Args:
        retry_count: Número atual de tentativas
        max_retries: Número máximo de tentativas permitidas
        error: Exceção que ocorreu
        
    Returns:
        True se deve tentar novamente, False caso contrário
    """
    if retry_count >= max_retries:
        return False
    
    # Erros que não devem ser retryados
    non_retryable_errors = (
        ValueError,
        TypeError,
        KeyError,
    )
    
    if isinstance(error, non_retryable_errors):
        return False
    
    return True


def merge_agent_results(
    accumulated: Dict[str, Any],
    new_results: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Mescla resultados de agentes de forma inteligente.

    Args:
        accumulated: Resultados acumulados anteriores
        new_results: Novos resultados a mesclar

    Returns:
        Dicionário com resultados mesclados
    """
    merged = accumulated.copy()

    for key, value in new_results.items():
        if key in merged:
            # Se ambos são dicionários, mesclar recursivamente
            if isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = merge_agent_results(merged[key], value)
            # Se ambos são listas, concatenar
            elif isinstance(merged[key], list) and isinstance(value, list):
                merged[key] = merged[key] + value
            # Caso contrário, sobrescrever
            else:
                merged[key] = value
        else:
            merged[key] = value

    return merged


def create_workflow_summary(workflow_state: Dict[str, Any]) -> str:
    """
    Cria um resumo do estado do workflow.

    Args:
        workflow_state: Estado do workflow

    Returns:
        String com resumo do workflow
    """
    status = workflow_state.get("status", "unknown")
    current_index = workflow_state.get("current_agent_index", 0)
    agent_sequence = workflow_state.get("agent_sequence", [])
    agent_executions = workflow_state.get("agent_executions", [])

    summary = f"Workflow Summary:\n"
    summary += f"  Status: {status}\n"
    summary += f"  Progress: {current_index}/{len(agent_sequence)} agents\n"
    summary += f"  Agent Sequence: {' -> '.join(agent_sequence)}\n"

    if agent_executions:
        completed = sum(1 for e in agent_executions if e.get("status") == "completed")
        failed = sum(1 for e in agent_executions if e.get("status") == "failed")
        summary += f"  Executions: {completed} completed, {failed} failed\n"

    return summary


def validate_agent_sequence(sequence: List[str], available_agents: List[str]) -> bool:
    """
    Valida se a sequência de agentes contém apenas agentes disponíveis.
    
    Args:
        sequence: Sequência de agentes a validar
        available_agents: Lista de agentes disponíveis
        
    Returns:
        True se válida, False caso contrário
    """
    return all(agent in available_agents for agent in sequence)


def calculate_workflow_progress(
    current_index: int, 
    total_agents: int
) -> float:
    """
    Calcula o progresso do workflow como porcentagem.
    
    Args:
        current_index: Índice atual do agente
        total_agents: Total de agentes na sequência
        
    Returns:
        Progresso como porcentagem (0-100)
    """
    if total_agents == 0:
        return 0.0
    
    return (current_index / total_agents) * 100


def is_timeout_exceeded(
    start_time: datetime, 
    timeout_seconds: int
) -> bool:
    """
    Verifica se o timeout foi excedido.
    
    Args:
        start_time: Timestamp de início
        timeout_seconds: Timeout em segundos
        
    Returns:
        True se timeout excedido, False caso contrário
    """
    elapsed = (datetime.utcnow() - start_time).total_seconds()
    return elapsed >= timeout_seconds


def format_error_message(error: Exception, context: Optional[Dict] = None) -> str:
    """
    Formata mensagem de erro com contexto.
    
    Args:
        error: Exceção que ocorreu
        context: Contexto adicional opcional
        
    Returns:
        String formatada com mensagem de erro
    """
    message = f"{type(error).__name__}: {str(error)}"
    
    if context:
        context_str = " | ".join(f"{k}={v}" for k, v in context.items())
        message = f"{message} | Context: {context_str}"
    
    return message


def get_agent_priority(agent_name: str) -> int:
    """
    Retorna prioridade de um agente para execução.
    Agentes com menor prioridade executam primeiro.
    
    Args:
        agent_name: Nome do agente
        
    Returns:
        Nível de prioridade (menor = mais prioritário)
    """
    priority_map = {
        "architecture_agent": 1,
        "database_agent": 2,
        "backend_agent": 3,
        "frontend_agent": 4,
        "etl_agent": 5,
        "analytics_agent": 6,
        "ml_agent": 7,
        "testing_agent": 8,
        "documentation_agent": 9,
        "deployment_agent": 10
    }
    
    return priority_map.get(agent_name, 99)


def sort_agents_by_priority(agents: List[str]) -> List[str]:
    """
    Ordena lista de agentes por prioridade.
    
    Args:
        agents: Lista de nomes de agentes
        
    Returns:
        Lista ordenada por prioridade
    """
    return sorted(agents, key=get_agent_priority)


def create_error_response(
    agent_name: str, 
    error: Exception, 
    execution_time: float
) -> Dict[str, Any]:
    """
    Cria resposta de erro padronizada.
    
    Args:
        agent_name: Nome do agente que falhou
        error: Exceção que ocorreu
        execution_time: Tempo de execução até o erro
        
    Returns:
        Dicionário com resposta de erro padronizada
    """
    return {
        "agent_name": agent_name,
        "success": False,
        "error": {
            "type": type(error).__name__,
            "message": str(error),
            "timestamp": datetime.utcnow().isoformat()
        },
        "execution_time": execution_time
    }


def create_success_response(
    agent_name: str, 
    result: Dict[str, Any], 
    execution_time: float
) -> Dict[str, Any]:
    """
    Cria resposta de sucesso padronizada.
    
    Args:
        agent_name: Nome do agente que executou
        result: Resultado da execução
        execution_time: Tempo de execução
        
    Returns:
        Dicionário com resposta de sucesso padronizada
    """
    return {
        "agent_name": agent_name,
        "success": True,
        "result": result,
        "execution_time": execution_time,
        "timestamp": datetime.utcnow().isoformat()
    }
