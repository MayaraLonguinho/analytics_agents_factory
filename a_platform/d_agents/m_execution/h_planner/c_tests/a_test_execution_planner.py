"""
Tests for Execution Planner
"""

import pytest
import asyncio
from datetime import datetime
from ....planner.execution_planner import ExecutionPlanner
from ....planner.base_planner import BasePlanner
from ....schemas import OrchestrationInput, WorkflowConfig


class TestExecutionPlanner:
    """Testes para ExecutionPlanner"""

    @pytest.fixture
    def available_agents(self):
        """Agentes disponíveis para testes"""
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

    @pytest.fixture
    def planner(self, available_agents):
        """Instância do planner para testes"""
        config = WorkflowConfig()
        return ExecutionPlanner(available_agents, config)

    @pytest.fixture
    def sample_input(self):
        """Input de exemplo para testes"""
        return OrchestrationInput(
            requirements="Create an analytics dashboard with machine learning",
            project_name="test_project",
            priority="normal"
        )

    @pytest.mark.asyncio
    async def test_create_execution_plan(self, planner, sample_input):
        """Testa criação de plano de execução"""
        plan = await planner.create_execution_plan(sample_input)

        assert plan is not None
        assert "workflow_id" in plan
        assert "agent_sequence" in plan
        assert "dependencies" in plan
        assert "parallel_groups" in plan
        assert "estimated_time" in plan
        assert len(plan["agent_sequence"]) > 0

    @pytest.mark.asyncio
    async def test_plan_with_analytics_requirements(self, planner):
        """Testa plano com requisitos de analytics"""
        input_data = OrchestrationInput(
            requirements="Create analytics dashboard with reports",
            project_name="analytics_project"
        )

        plan = await planner.create_execution_plan(input_data)

        assert "analytics_agent" in plan["agent_sequence"]
        assert "architecture_agent" in plan["agent_sequence"]

    @pytest.mark.asyncio
    async def test_plan_with_ml_requirements(self, planner):
        """Testa plano com requisitos de ML"""
        input_data = OrchestrationInput(
            requirements="Build machine learning model for predictions",
            project_name="ml_project"
        )

        plan = await planner.create_execution_plan(input_data)

        assert "ml_agent" in plan["agent_sequence"]
        assert "etl_agent" in plan["agent_sequence"]

    @pytest.mark.asyncio
    async def test_plan_with_etl_requirements(self, planner):
        """Testa plano com requisitos de ETL"""
        input_data = OrchestrationInput(
            requirements="Create ETL pipeline for data processing",
            project_name="etl_project"
        )

        plan = await planner.create_execution_plan(input_data)

        assert "etl_agent" in plan["agent_sequence"]

    def test_validate_valid_plan(self, planner):
        """Testa validação de plano válido"""
        plan = {
            "workflow_id": "test-id",
            "agent_sequence": ["architecture_agent", "backend_agent"],
            "dependencies": {
                "backend_agent": ["architecture_agent"]
            },
            "parallel_groups": [["architecture_agent"], ["backend_agent"]]
        }

        assert planner.validate_plan(plan) is True

    def test_validate_invalid_plan_missing_fields(self, planner):
        """Testa validação de plano com campos faltando"""
        plan = {
            "workflow_id": "test-id"
        }

        assert planner.validate_plan(plan) is False

    def test_validate_invalid_plan_invalid_agent(self, planner):
        """Testa validação de plano com agente inválido"""
        plan = {
            "workflow_id": "test-id",
            "agent_sequence": ["invalid_agent"],
            "dependencies": {},
            "parallel_groups": [["invalid_agent"]]
        }

        assert planner.validate_plan(plan) is False

    def test_estimate_execution_time(self, planner):
        """Testa estimativa de tempo de execução"""
        plan = {
            "agent_sequence": ["architecture_agent", "backend_agent"],
            "parallel_groups": [["architecture_agent"], ["backend_agent"]]
        }

        estimated_time = planner.estimate_execution_time(plan)

        assert estimated_time > 0
        assert isinstance(estimated_time, float)

    def test_estimate_execution_time_parallel(self, planner):
        """Testa estimativa de tempo com execução paralela"""
        plan = {
            "agent_sequence": ["architecture_agent", "backend_agent"],
            "parallel_groups": [["architecture_agent", "backend_agent"]]
        }

        estimated_time = planner.estimate_execution_time(plan)

        # Tempo paralelo deve ser menor que sequencial
        sequential_plan = {
            "agent_sequence": ["architecture_agent", "backend_agent"],
            "parallel_groups": [["architecture_agent"], ["backend_agent"]]
        }
        sequential_time = planner.estimate_execution_time(sequential_plan)

        assert estimated_time < sequential_time

    def test_get_plan_summary(self, planner):
        """Testa geração de resumo do plano"""
        plan = {
            "workflow_id": "test-id",
            "agent_sequence": ["architecture_agent", "backend_agent"],
            "dependencies": {
                "backend_agent": ["architecture_agent"]
            },
            "parallel_groups": [["architecture_agent"], ["backend_agent"]],
            "estimated_time": 180.0
        }

        summary = planner.get_plan_summary(plan)

        assert "Execution Plan Summary" in summary
        assert "architecture_agent" in summary
        assert "backend_agent" in summary
        assert "180.0" in summary


class TestBasePlanner:
    """Testes para BasePlanner"""

    @pytest.fixture
    def available_agents(self):
        """Agentes disponíveis para testes"""
        return [
            "architecture_agent",
            "database_agent",
            "backend_agent"
        ]

    @pytest.fixture
    def planner(self, available_agents):
        """Instância do planner base para testes"""
        return BasePlanner(available_agents)

    def test_load_agent_capabilities(self, planner):
        """Testa carregamento de capacidades dos agentes"""
        capabilities = planner.agent_capabilities

        assert isinstance(capabilities, dict)
        assert len(capabilities) > 0
        assert "architecture_agent" in capabilities

    def test_build_dependency_graph(self, planner):
        """Testa construção de grafo de dependências"""
        sequence = ["architecture_agent", "database_agent", "backend_agent"]
        graph = planner._build_dependency_graph(sequence)

        assert graph.nodes == sequence
        assert len(graph.edges) > 0

    def test_calculate_parallel_groups(self, planner):
        """Testa cálculo de grupos paralelos"""
        sequence = ["architecture_agent", "database_agent", "backend_agent"]
        graph = planner._build_dependency_graph(sequence)
        groups = planner._calculate_parallel_groups(graph)

        assert isinstance(groups, list)
        assert len(groups) > 0
        assert all(isinstance(group, list) for group in groups)

    def test_validate_agent_sequence_valid(self, planner):
        """Testa validação de sequência válida"""
        sequence = ["architecture_agent", "database_agent"]
        assert planner._validate_agent_sequence(sequence) is True

    def test_validate_agent_sequence_invalid(self, planner):
        """Testa validação de sequência inválida"""
        sequence = ["architecture_agent", "invalid_agent"]
        assert planner._validate_agent_sequence(sequence) is False

    def test_get_default_sequence(self, planner):
        """Testa obtenção de sequência padrão"""
        sequence = planner._get_default_sequence()

        assert isinstance(sequence, list)
        assert len(sequence) > 0
        assert "architecture_agent" in sequence

    def test_filter_sequence_by_requirements_analytics(self, planner):
        """Testa filtro de sequência por requisitos de analytics"""
        requirements = "Create analytics dashboard"
        default_sequence = planner._get_default_sequence()
        filtered = planner._filter_sequence_by_requirements(requirements, default_sequence)

        assert "analytics_agent" in filtered
        assert "architecture_agent" in filtered

    def test_filter_sequence_by_requirements_backend(self, planner):
        """Testa filtro de sequência por requisitos de backend"""
        requirements = "Create REST API backend"
        default_sequence = planner._get_default_sequence()
        filtered = planner._filter_sequence_by_requirements(requirements, default_sequence)

        assert "backend_agent" in filtered
        assert "architecture_agent" in filtered
