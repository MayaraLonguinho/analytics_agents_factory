"""
Agent Assigner - Atribuição de agentes a tarefas
"""

from typing import List, Optional, Dict
from .interfaces import IAgentAssigner
from .schemas import Task, PlanningContext


class AgentAssigner(IAgentAssigner):
    """Implementação de atribuição de agentes."""

    # Mapeamento de tipo de tarefa para agente padrão
    DEFAULT_AGENTS = {
        "data_collection": "data_agent",
        "data_processing": "data_agent",
        "analysis": "analytics_agent",
        "calculation": "analytics_agent",
        "validation": "analytics_agent",
        "reporting": "reporting_agent",
        "notification": "notification_agent",
        "custom": "general_agent"
    }

    async def assign(self, task: Task, available_agents: List[str], context: Optional[PlanningContext] = None) -> str:
        """Atribui um agente a uma tarefa."""
        # Se já tem agente atribuído, verificar se está disponível
        if task.responsible_agent and task.responsible_agent in available_agents:
            return task.responsible_agent

        # Se contexto tem capacidades de agentes, usar
        if context and context.agent_capabilities:
            return self._assign_by_capability(task, context)

        # Usar agente padrão baseado no tipo
        default_agent = self.DEFAULT_AGENTS.get(task.task_type.value, "general_agent")

        # Verificar se está disponível
        if default_agent in available_agents:
            return default_agent

        # Se não, retornar primeiro agente disponível
        if available_agents:
            return available_agents[0]

        # Fallback
        return "general_agent"

    async def assign_all(self, tasks: List[Task], context: Optional[PlanningContext] = None) -> List[Task]:
        """Atribui agentes a todas as tarefas."""
        available_agents = context.available_agents if context else []

        for task in tasks:
            agent = await self.assign(task, available_agents, context)
            task.responsible_agent = agent

        return tasks

    async def balance_load(self, tasks: List[Task], context: Optional[PlanningContext] = None) -> List[Task]:
        """Balanceia a carga entre agentes."""
        available_agents = context.available_agents if context else []

        if not available_agents:
            return tasks

        # Contar tarefas por agente
        agent_task_count: Dict[str, int] = {agent: 0 for agent in available_agents}

        # Reatribuir tarefas para balancear
        for task in tasks:
            # Atribuir ao agente com menos carga
            least_loaded_agent = min(agent_task_count.keys(), key=lambda a: agent_task_count[a])
            task.responsible_agent = least_loaded_agent
            agent_task_count[least_loaded_agent] += 1

        return tasks

    def _assign_by_capability(self, task: Task, context: PlanningContext) -> str:
        """Atribui agente baseado em capacidades."""
        for agent, capabilities in context.agent_capabilities.items():
            if task.task_type.value in capabilities:
                return agent

        # Fallback para agente padrão
        return self.DEFAULT_AGENTS.get(task.task_type.value, "general_agent")
