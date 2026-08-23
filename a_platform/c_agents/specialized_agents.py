import logging
from typing import List, Dict, Any

from a_platform.c_agents.base_agent import BaseAgent
from a_platform.a_core.b_domain.project_plan import Task
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.artifact import Artifact

logger = logging.getLogger(__name__)


class DataAgent(BaseAgent):
    """
    Especialista em Ingestão e ETL.
    """
    def execute_task(self, task: Task, request: ProjectRequest) -> List[Artifact]:
        logger.info(f"[{self.name}] Executando task especializada de engenharia de dados: {task.name}")
        # Filtrar apenas skills relevantes ao domínio
        relevant_skills = ["dataset_profiling", "etl_scripting"]
        task.skills = [s for s in task.skills if s in relevant_skills] or relevant_skills
        return super().execute_task(task, request)


class DatabaseAgent(BaseAgent):
    """
    Especialista em modelagem de dados e DDL.
    """
    def execute_task(self, task: Task, request: ProjectRequest) -> List[Artifact]:
        logger.info(f"[{self.name}] Executando task especializada de banco de dados: {task.name}")
        relevant_skills = ["sql_generation"]
        task.skills = [s for s in task.skills if s in relevant_skills] or relevant_skills
        return super().execute_task(task, request)


class AnalyticsAgent(BaseAgent):
    """
    Especialista em métricas, queries SQL complexas e visualização.
    """
    def execute_task(self, task: Task, request: ProjectRequest) -> List[Artifact]:
        logger.info(f"[{self.name}] Executando task analítica: {task.name}")
        relevant_skills = ["sql_generation", "basic_coding"]
        task.skills = [s for s in task.skills if s in relevant_skills] or relevant_skills
        return super().execute_task(task, request)


class TestingAgent(BaseAgent):
    """
    Especialista em qualidade e testes de unidade/integração.
    """
    def execute_task(self, task: Task, request: ProjectRequest) -> List[Artifact]:
        logger.info(f"[{self.name}] Executando task especializada de testes: {task.name}")
        relevant_skills = ["basic_coding"]
        task.skills = [s for s in task.skills if s in relevant_skills] or relevant_skills
        return super().execute_task(task, request)


class InfrastructureAgent(BaseAgent):
    """
    Especialista em infraestrutura como código (Docker, Terraform).
    """
    def execute_task(self, task: Task, request: ProjectRequest) -> List[Artifact]:
        logger.info(f"[{self.name}] Executando task especializada de infraestrutura: {task.name}")
        relevant_skills = ["basic_coding"]
        task.skills = [s for s in task.skills if s in relevant_skills] or relevant_skills
        return super().execute_task(task, request)


class BackendAgent(BaseAgent):
    def execute_task(self, task: Task, request: ProjectRequest) -> List[Artifact]:
        logger.info(f"[{self.name}] Executando task especializada de backend: {task.name}")
        relevant_skills = ["api_design", "basic_coding"]
        task.skills = [s for s in task.skills if s in relevant_skills] or relevant_skills
        return super().execute_task(task, request)


class FrontendAgent(BaseAgent):
    def execute_task(self, task: Task, request: ProjectRequest) -> List[Artifact]:
        logger.info(f"[{self.name}] Executando task especializada de frontend: {task.name}")
        relevant_skills = ["api_design", "basic_coding"]
        task.skills = [s for s in task.skills if s in relevant_skills] or relevant_skills
        return super().execute_task(task, request)
