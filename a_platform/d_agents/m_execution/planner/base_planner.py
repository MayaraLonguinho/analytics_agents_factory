"""
Base Planner - Interface base para planners
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from ...interfaces import IPlanner
from ...schemas import DependencyGraph


class BasePlanner(IPlanner, ABC):
    """
    Classe base para planners de execução.
    Implementa funcionalidades comuns de planejamento.
    """

    def __init__(self, available_agents: List[str]):
        """
        Inicializa o planner.

        Args:
            available_agents: Lista de agentes disponíveis no sistema
        """
        self.available_agents = available_agents
        self.agent_capabilities = self._load_agent_capabilities()

    def _load_agent_capabilities(self) -> Dict[str, Dict[str, Any]]:
        """
        Carrega capacidades dos agentes disponíveis.

        Returns:
            Dicionário com capacidades de cada agente
        """
        capabilities = {
            "architecture_agent": {
                "input_requirements": ["requirements", "project_name"],
                "output_provides": ["architecture", "tech_stack", "module_structure"],
                "estimated_time": 60.0,
                "dependencies": []
            },
            "database_agent": {
                "input_requirements": ["architecture"],
                "output_provides": ["database_schema", "migrations"],
                "estimated_time": 45.0,
                "dependencies": ["architecture_agent"]
            },
            "backend_agent": {
                "input_requirements": ["architecture", "database_schema"],
                "output_provides": ["backend_code", "api_endpoints"],
                "estimated_time": 120.0,
                "dependencies": ["architecture_agent", "database_agent"]
            },
            "frontend_agent": {
                "input_requirements": ["architecture", "api_endpoints"],
                "output_provides": ["frontend_code", "ui_components"],
                "estimated_time": 120.0,
                "dependencies": ["architecture_agent", "backend_agent"]
            },
            "etl_agent": {
                "input_requirements": ["architecture", "database_schema"],
                "output_provides": ["etl_pipelines", "data_jobs"],
                "estimated_time": 90.0,
                "dependencies": ["architecture_agent", "database_agent"]
            },
            "analytics_agent": {
                "input_requirements": ["etl_pipelines", "database_schema"],
                "output_provides": ["dashboards", "reports", "metrics"],
                "estimated_time": 90.0,
                "dependencies": ["etl_agent"]
            },
            "ml_agent": {
                "input_requirements": ["etl_pipelines", "database_schema"],
                "output_provides": ["ml_models", "inference_pipelines"],
                "estimated_time": 120.0,
                "dependencies": ["etl_agent"]
            },
            "testing_agent": {
                "input_requirements": ["backend_code", "frontend_code"],
                "output_provides": ["unit_tests", "integration_tests"],
                "estimated_time": 60.0,
                "dependencies": ["backend_agent", "frontend_agent"]
            },
            "documentation_agent": {
                "input_requirements": ["architecture", "backend_code", "frontend_code"],
                "output_provides": ["readme", "api_docs", "guides"],
                "estimated_time": 45.0,
                "dependencies": ["architecture_agent", "backend_agent", "frontend_agent"]
            },
            "deployment_agent": {
                "input_requirements": ["backend_code", "frontend_code", "unit_tests"],
                "output_provides": ["dockerfiles", "ci_cd_config", "deployment_scripts"],
                "estimated_time": 60.0,
                "dependencies": ["backend_agent", "frontend_agent", "testing_agent"]
            }
        }

        # Filtrar apenas agentes disponíveis
        return {
            agent: capabilities[agent]
            for agent in self.available_agents
            if agent in capabilities
        }

    def _build_dependency_graph(self, agent_sequence: List[str]) -> DependencyGraph:
        """
        Constrói grafo de dependências baseado nas capacidades dos agentes.

        Args:
            agent_sequence: Sequência de agentes

        Returns:
            DependencyGraph com dependências
        """
        graph = DependencyGraph()

        for agent in agent_sequence:
            graph.add_node(agent)

        for agent in agent_sequence:
            if agent in self.agent_capabilities:
                deps = self.agent_capabilities[agent].get("dependencies", [])
                for dep in deps:
                    if dep in agent_sequence:
                        graph.add_edge(dep, agent)

        return graph

    def _calculate_parallel_groups(
        self,
        graph: DependencyGraph
    ) -> List[List[str]]:
        """
        Calcula grupos de agentes que podem executar em paralelo.

        Args:
            graph: Grafo de dependências

        Returns:
            Lista de grupos de agentes paralelos
        """
        groups = []
        remaining = set(graph.nodes)

        while remaining:
            # Encontrar agentes sem dependências pendentes
            ready = []
            for agent in remaining:
                deps = graph.get_dependencies(agent)
                if all(dep not in remaining for dep in deps):
                    ready.append(agent)

            if not ready:
                # Ciclo detectado, usar ordem original
                ready = [list(remaining)[0]]

            groups.append(ready)
            remaining -= set(ready)

        return groups

    def _validate_agent_sequence(self, sequence: List[str]) -> bool:
        """
        Valida se a sequência de agentes é válida.

        Args:
            sequence: Sequência de agentes

        Returns:
            True se válida, False caso contrário
        """
        return all(agent in self.available_agents for agent in sequence)

    def _get_default_sequence(self) -> List[str]:
        """
        Retorna sequência padrão de agentes.

        Returns:
            Lista de agentes em ordem padrão
        """
        return [
            "architecture_agent",
            "database_agent",
            "backend_agent",
            "frontend_agent",
            "etl_agent",
            "analytics_agent",
            "ml_agent",
            "testing_agent",
            "documentation_agent",
            "deployment_agent"
        ]

    def _filter_sequence_by_requirements(
        self,
        requirements: str,
        default_sequence: List[str]
    ) -> List[str]:
        """
        Filtra sequência de agentes baseado nos requisitos.

        Args:
            requirements: Requisitos em linguagem natural
            default_sequence: Sequência padrão

        Returns:
            Sequência filtrada
        """
        # Análise simples de requisitos para determinar agentes necessários
        requirements_lower = requirements.lower()

        keywords_to_agents = {
            "analytics": ["analytics_agent"],
            "dashboard": ["analytics_agent"],
            "report": ["analytics_agent"],
            "machine learning": ["ml_agent"],
            "ml": ["ml_agent"],
            "model": ["ml_agent"],
            "etl": ["etl_agent"],
            "pipeline": ["etl_agent"],
            "data": ["etl_agent", "analytics_agent"],
            "api": ["backend_agent"],
            "backend": ["backend_agent"],
            "frontend": ["frontend_agent"],
            "ui": ["frontend_agent"],
            "database": ["database_agent"],
            "test": ["testing_agent"],
            "deploy": ["deployment_agent"],
            "documentation": ["documentation_agent"],
            "docs": ["documentation_agent"]
        }

        required_agents = set()
        for keyword, agents in keywords_to_agents.items():
            if keyword in requirements_lower:
                required_agents.update(agents)

        # Sempre incluir architecture_agent
        required_agents.add("architecture_agent")

        # Adicionar dependências
        final_sequence = []
        for agent in default_sequence:
            if agent in required_agents:
                # Adicionar dependências primeiro
                if agent in self.agent_capabilities:
                    deps = self.agent_capabilities[agent].get("dependencies", [])
                    for dep in deps:
                        if dep not in final_sequence and dep in required_agents:
                            final_sequence.append(dep)
                if agent not in final_sequence:
                    final_sequence.append(agent)

        return final_sequence if final_sequence else default_sequence
