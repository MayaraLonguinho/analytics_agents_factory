"""
Execution Planner - Implementação do planner de execução
"""

import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from .a_base_planner import BasePlanner
from ...schemas import (
    OrchestrationInput,
    ExecutionPlan,
    WorkflowConfig
)
from ...utils import generate_workflow_id


class ExecutionPlanner(BasePlanner):
    """
    Implementação do planner de execução.
    Responsável por interpretar requisitos e criar planos de execução.
    """

    def __init__(
        self,
        available_agents: List[str],
        default_config: Optional[WorkflowConfig] = None
    ):
        """
        Inicializa o ExecutionPlanner.

        Args:
            available_agents: Lista de agentes disponíveis
            default_config: Configuração padrão de workflow
        """
        super().__init__(available_agents)
        self.default_config = default_config or WorkflowConfig()

    async def create_execution_plan(
        self,
        input_data: OrchestrationInput
    ) -> Dict[str, Any]:
        """
        Cria um plano de execução baseado nos requisitos.

        Args:
            input_data: Dados de entrada da orquestração

        Returns:
            Dicionário com plano de execução
        """
        workflow_id = generate_workflow_id()

        # Determinar sequência de agentes baseado nos requisitos
        default_sequence = self._get_default_sequence()
        agent_sequence = self._filter_sequence_by_requirements(
            input_data.requirements,
            default_sequence
        )

        # Validar sequência
        if not self._validate_agent_sequence(agent_sequence):
            raise ValueError(
                f"Invalid agent sequence. Available agents: {self.available_agents}"
            )

        # Construir grafo de dependências
        dependency_graph = self._build_dependency_graph(agent_sequence)

        # Calcular grupos paralelos
        parallel_groups = self._calculate_parallel_groups(dependency_graph)

        # Construir mapa de dependências
        dependencies = {}
        for agent in agent_sequence:
            dependencies[agent] = dependency_graph.get_dependencies(agent)

        # Calcular inputs requeridos
        required_inputs = self._calculate_required_inputs(agent_sequence)

        # Estimar tempo de execução
        estimated_time = self.estimate_execution_time({
            "agent_sequence": agent_sequence,
            "parallel_groups": parallel_groups
        })

        # Criar plano
        plan = ExecutionPlan(
            workflow_id=workflow_id,
            agent_sequence=agent_sequence,
            dependencies=dependencies,
            parallel_groups=parallel_groups,
            estimated_time=estimated_time,
            required_inputs=required_inputs,
            config=self._merge_config(input_data.config)
        )

        return plan.dict()

    def validate_plan(self, plan: Dict[str, Any]) -> bool:
        """
        Valida se um plano de execução é válido.

        Args:
            plan: Plano de execução a validar

        Returns:
            True se válido, False caso contrário
        """
        try:
            # Validar campos obrigatórios
            required_fields = [
                "workflow_id",
                "agent_sequence",
                "dependencies",
                "parallel_groups"
            ]

            for field in required_fields:
                if field not in plan:
                    return False

            # Validar sequência de agentes
            agent_sequence = plan["agent_sequence"]
            if not isinstance(agent_sequence, list) or not agent_sequence:
                return False

            if not self._validate_agent_sequence(agent_sequence):
                return False

            # Validar dependências
            dependencies = plan["dependencies"]
            if not isinstance(dependencies, dict):
                return False

            for agent, deps in dependencies.items():
                if not isinstance(deps, list):
                    return False
                if agent not in agent_sequence:
                    return False
                for dep in deps:
                    if dep not in agent_sequence:
                        return False

            # Validar grupos paralelos
            parallel_groups = plan["parallel_groups"]
            if not isinstance(parallel_groups, list):
                return False

            all_agents_in_groups = []
            for group in parallel_groups:
                if not isinstance(group, list):
                    return False
                all_agents_in_groups.extend(group)

            # Verificar se todos os agentes estão nos grupos
            if set(agent_sequence) != set(all_agents_in_groups):
                return False

            return True

        except Exception:
            return False

    def estimate_execution_time(self, plan: Dict[str, Any]) -> float:
        """
        Estima o tempo de execução de um plano.

        Args:
            plan: Plano de execução

        Returns:
            Tempo estimado em segundos
        """
        agent_sequence = plan.get("agent_sequence", [])
        parallel_groups = plan.get("parallel_groups", [])

        if not parallel_groups:
            # Se não há grupos paralelos, soma sequencial
            total_time = 0.0
            for agent in agent_sequence:
                if agent in self.agent_capabilities:
                    total_time += self.agent_capabilities[agent]["estimated_time"]
            return total_time

        # Calcular tempo baseado em grupos paralelos
        total_time = 0.0
        for group in parallel_groups:
            # Tempo do grupo é o máximo dos agentes no grupo
            group_time = 0.0
            for agent in group:
                if agent in self.agent_capabilities:
                    agent_time = self.agent_capabilities[agent]["estimated_time"]
                    group_time = max(group_time, agent_time)
            total_time += group_time

        return total_time

    def _calculate_required_inputs(
        self,
        agent_sequence: List[str]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Calcula inputs requeridos por cada agente.

        Args:
            agent_sequence: Sequência de agentes

        Returns:
            Dicionário com inputs requeridos por agente
        """
        required_inputs = {}

        for agent in agent_sequence:
            if agent in self.agent_capabilities:
                capabilities = self.agent_capabilities[agent]
                required_inputs[agent] = {
                    "requirements": capabilities.get("input_requirements", []),
                    "provided_by": self._get_input_providers(agent, agent_sequence)
                }

        return required_inputs

    def _get_input_providers(
        self,
        agent: str,
        agent_sequence: List[str]
    ) -> List[str]:
        """
        Determina quais agentes fornecem inputs para este agente.

        Args:
            agent: Agente alvo
            agent_sequence: Sequência de agentes

        Returns:
            Lista de agentes que fornecem inputs
        """
        providers = []

        if agent not in self.agent_capabilities:
            return providers

        input_requirements = self.agent_capabilities[agent].get("input_requirements", [])

        for other_agent in agent_sequence:
            if other_agent == agent:
                continue

            if other_agent in self.agent_capabilities:
                other_provides = self.agent_capabilities[other_agent].get(
                    "output_provides",
                    []
                )

                # Verificar se há sobreposição
                if any(req in other_provides for req in input_requirements):
                    providers.append(other_agent)

        return providers

    def _merge_config(
        self,
        user_config: Optional[Dict[str, Any]]
    ) -> WorkflowConfig:
        """
        Mescla configuração do usuário com configuração padrão.

        Args:
            user_config: Configuração fornecida pelo usuário

        Returns:
            WorkflowConfig mesclada
        """
        if not user_config:
            return self.default_config

        config_dict = self.default_config.dict()

        # Atualizar com configuração do usuário
        for key, value in user_config.items():
            if key in config_dict and isinstance(config_dict[key], type(value)):
                config_dict[key] = value

        return WorkflowConfig(**config_dict)

    def _analyze_requirements_complexity(self, requirements: str) -> str:
        """
        Analisa a complexidade dos requisitos.

        Args:
            requirements: Requisitos em linguagem natural

        Returns:
            Nível de complexidade (low, medium, high)
        """
        # Contar palavras e frases
        word_count = len(re.findall(r'\w+', requirements))
        sentence_count = len(re.findall(r'[.!?]+', requirements))

        # Palavras-chave de complexidade
        complex_keywords = [
            "integration", "distributed", "scalable", "real-time",
            "machine learning", "artificial intelligence", "advanced",
            "complex", "enterprise", "microservices"
        ]

        complex_count = sum(
            1 for keyword in complex_keywords
            if keyword.lower() in requirements.lower()
        )

        # Determinar complexidade
        if word_count < 50 and complex_count == 0:
            return "low"
        elif word_count < 200 and complex_count <= 2:
            return "medium"
        else:
            return "high"

    def get_plan_summary(self, plan: Dict[str, Any]) -> str:
        """
        Gera um resumo do plano de execução.

        Args:
            plan: Plano de execução

        Returns:
            String com resumo do plano
        """
        agent_sequence = plan.get("agent_sequence", [])
        parallel_groups = plan.get("parallel_groups", [])
        estimated_time = plan.get("estimated_time", 0.0)

        summary = f"Execution Plan Summary:\n"
        summary += f"  - Total Agents: {len(agent_sequence)}\n"
        summary += f"  - Parallel Groups: {len(parallel_groups)}\n"
        summary += f"  - Estimated Time: {estimated_time:.1f}s\n"
        summary += f"  - Agent Sequence: {' -> '.join(agent_sequence)}\n"

        if parallel_groups:
            summary += "\nParallel Execution Groups:\n"
            for i, group in enumerate(parallel_groups, 1):
                summary += f"  Group {i}: {', '.join(group)}\n"

        return summary
