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
        
        # Inject domain rules
        domain_rules = "REGRAS DE DADOS/ETL: Você deve incluir regras rígidas de sanitização e tratar possíveis valores nulos ou duplicados. Invoque as ferramentas de profiling se necessário."
        task.description = f"{task.description}\n\n{domain_rules}"
        
        return super().execute_task(task, request)


class DatabaseAgent(BaseAgent):
    """
    Especialista em modelagem de dados e DDL.
    """
    def execute_task(self, task: Task, request: ProjectRequest) -> List[Artifact]:
        logger.info(f"[{self.name}] Executando task especializada de banco de dados: {task.name}")
        relevant_skills = ["sql_generation"]
        task.skills = [s for s in task.skills if s in relevant_skills] or relevant_skills
        
        domain_rules = "REGRAS DE BANCO DE DADOS: O código SQL deve obrigatoriamente incluir constraints (Primary Keys, Foreign Keys, Not Null, etc.) e seguir boas práticas de DDL."
        task.description = f"{task.description}\n\n{domain_rules}"
        
        return super().execute_task(task, request)


class AnalyticsAgent(BaseAgent):
    """
    Especialista em métricas, queries SQL complexas e visualização.
    """
    def execute_task(self, task: Task, request: ProjectRequest) -> List[Artifact]:
        logger.info(f"[{self.name}] Executando task analítica: {task.name}")
        relevant_skills = ["sql_generation", "basic_coding"]
        task.skills = [s for s in task.skills if s in relevant_skills] or relevant_skills
        
        domain_rules = "REGRAS ANALÍTICAS: Estruture queries focadas em performance, utilizando CTEs para legibilidade e implementando métricas analíticas claras."
        task.description = f"{task.description}\n\n{domain_rules}"
        
        return super().execute_task(task, request)


class TestingAgent(BaseAgent):
    """
    Especialista em qualidade e testes de unidade/integração.
    """
    def execute_task(self, task: Task, request: ProjectRequest) -> List[Artifact]:
        logger.info(f"[{self.name}] Executando task especializada de testes: {task.name}")
        relevant_skills = ["basic_coding"]
        task.skills = [s for s in task.skills if s in relevant_skills] or relevant_skills
        
        domain_rules = "REGRAS DE TESTING: Escreva asserções claras cobrindo os schemas ou lógicas geradas. Utilize o padrão do `pytest` se for em Python."
        task.description = f"{task.description}\n\n{domain_rules}"
        
        return super().execute_task(task, request)


class InfrastructureAgent(BaseAgent):
    """
    Especialista em infraestrutura como código (Docker, Terraform).
    """
    def execute_task(self, task: Task, request: ProjectRequest) -> List[Artifact]:
        logger.info(f"[{self.name}] Executando task especializada de infraestrutura: {task.name}")
        relevant_skills = ["basic_coding"]
        task.skills = [s for s in task.skills if s in relevant_skills] or relevant_skills
        
        domain_rules = "REGRAS DE INFRA: Valide artefatos como Dockerfile, garanta dependências corretas (multi-stage build quando possível) e segurança."
        task.description = f"{task.description}\n\n{domain_rules}"
        
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
