import logging
from typing import List, Dict, Any

from a_platform.d_agents.base_agent import BaseAgent
from a_platform.a_core.b_domain.project_plan import Task
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.artifact import Artifact

logger = logging.getLogger(__name__)

def inject_dependencies(task: Task, request: ProjectRequest) -> str:
    if not request.artifacts:
        return ""
    
    text = "\n\nARTEFATOS JÁ GERADOS NO PROJETO (Use como contexto e dependência para sua tarefa):\n"
    for art in request.artifacts:
        if art.type in ["source_code", "skill_output"] and art.content:
            text += f"\n--- Arquivo: {art.name} ---\n{art.content}\n"
    return text


class DataAgent(BaseAgent):
    """
    Especialista em Ingestão e ETL.
    """
    def execute_task(self, task: Task, request: ProjectRequest) -> List[Artifact]:
        logger.info(f"[{self.name}] Executando task especializada de engenharia de dados: {task.name}")
        relevant_skills = ["dataset_profiling", "etl_scripting"]
        task.skills = [s for s in task.skills if s in relevant_skills] or relevant_skills
        
        domain_rules = (
            "REGRAS DE DADOS/ETL: Você deve orquestrar a geração de scripts ETL reais (etl.py ou pipeline.py). "
            "Os scripts devem ler dados da fonte informada, aplicar as transformações e limpezas baseadas no profiling, "
            "e persistir os dados no destino apropriado (SQLite, DuckDB ou PostgreSQL). "
            "É obrigatório o uso de tipagem (type hints) e blocos try/except para tratamento de erros."
        )
        task.description = f"{task.description}\n\n{domain_rules}{inject_dependencies(task, request)}"
        
        artifacts = super().execute_task(task, request)
        
        if not any(a.name.endswith('.py') for a in artifacts):
            raise ValueError(f"[{self.name}] Falha na validação: Nenhum script ETL (.py) foi gerado.")
            
        return artifacts


class DatabaseAgent(BaseAgent):
    """
    Especialista em modelagem de dados e DDL.
    """
    def execute_task(self, task: Task, request: ProjectRequest) -> List[Artifact]:
        logger.info(f"[{self.name}] Executando task especializada de banco de dados: {task.name}")
        relevant_skills = ["sql_generation"]
        task.skills = [s for s in task.skills if s in relevant_skills] or relevant_skills
        
        domain_rules = (
            "REGRAS DE BANCO DE DADOS: Você deve gerar artefatos DDL/SQL completos (ex: schema.sql ou init.sql). "
            "O código deve obrigatoriamente incluir todas as constraints (Primary Keys, Foreign Keys, Not Null), "
            "refletir exatamente os tipos de dados descobertos no profiling/discovery, "
            "e incluir scripts de migrations e seeds caso solicitados no contexto."
        )
        task.description = f"{task.description}\n\n{domain_rules}{inject_dependencies(task, request)}"
        
        artifacts = super().execute_task(task, request)
        
        if not any(a.name.endswith('.sql') or 'schema' in a.name.lower() for a in artifacts):
            raise ValueError(f"[{self.name}] Falha na validação: Nenhum script SQL DDL foi gerado.")
            
        return artifacts


class AnalyticsAgent(BaseAgent):
    """
    Especialista em métricas, queries SQL complexas e visualização.
    """
    def execute_task(self, task: Task, request: ProjectRequest) -> List[Artifact]:
        logger.info(f"[{self.name}] Executando task analítica: {task.name}")
        relevant_skills = ["sql_generation", "basic_coding"]
        task.skills = [s for s in task.skills if s in relevant_skills] or relevant_skills
        
        domain_rules = (
            "REGRAS ANALÍTICAS: Você deve gerar queries analíticas consolidadas (queries.sql ou analytics.py). "
            "Estruture visões analíticas focadas em performance utilizando CTEs para legibilidade. "
            "Você deve implementar as agregações matemáticas e o cálculo formal dos KPIs e métricas solicitados no Discovery."
        )
        task.description = f"{task.description}\n\n{domain_rules}{inject_dependencies(task, request)}"
        
        artifacts = super().execute_task(task, request)
        
        if not any(a.name.endswith('.sql') or a.name.endswith('.py') for a in artifacts):
            raise ValueError(f"[{self.name}] Falha na validação: Nenhum script analítico (.sql ou .py) foi gerado.")
            
        return artifacts


class TestingAgent(BaseAgent):
    """
    Especialista em qualidade e testes de unidade/integração.
    """
    def execute_task(self, task: Task, request: ProjectRequest) -> List[Artifact]:
        logger.info(f"[{self.name}] Executando task especializada de testes: {task.name}")
        relevant_skills = ["basic_coding"]
        task.skills = [s for s in task.skills if s in relevant_skills] or relevant_skills
        
        domain_rules = (
            "REGRAS DE TESTING: Você deve inspecionar os artefatos de código produzidos pelas tarefas anteriores "
            "(fornecidos no contexto) e gerar suítes pytest reais (ex: test_etl.py, test_api.py, test_database.py). "
            "É proibido gerar testes vazios ou stubs mockados sem utilidade. As asserções devem ser funcionais e "
            "validar a lógica exata do código gerado anteriormente."
        )
        task.description = f"{task.description}\n\n{domain_rules}{inject_dependencies(task, request)}"
        
        artifacts = super().execute_task(task, request)
        
        if not any(a.name.startswith('test_') or a.name.endswith('_test.py') for a in artifacts):
            raise ValueError(f"[{self.name}] Falha na validação: Nenhuma suíte de testes (test_*.py) foi gerada.")
            
        return artifacts


class InfrastructureAgent(BaseAgent):
    """
    Especialista em infraestrutura como código (Docker, Terraform).
    """
    def execute_task(self, task: Task, request: ProjectRequest) -> List[Artifact]:
        logger.info(f"[{self.name}] Executando task especializada de infraestrutura: {task.name}")
        relevant_skills = ["basic_coding"]
        task.skills = [s for s in task.skills if s in relevant_skills] or relevant_skills
        
        domain_rules = (
            "REGRAS DE INFRA: Se exigido pela arquitetura, crie arquivos de infraestrutura válidos. "
            "Gere um Dockerfile otimizado e um docker-compose.yml multi-serviço capaz de orquestrar o banco de dados, "
            "o backend e o frontend (se aplicável), englobando todos os artefatos já gerados com as dependências corretas."
        )
        task.description = f"{task.description}\n\n{domain_rules}{inject_dependencies(task, request)}"
        
        artifacts = super().execute_task(task, request)
        
        if not any('docker' in a.name.lower() or a.name.endswith('.yml') or a.name.endswith('.yaml') for a in artifacts):
            raise ValueError(f"[{self.name}] Falha na validação: Nenhum arquivo Docker ou de orquestração foi gerado.")
            
        return artifacts


class BackendAgent(BaseAgent):
    def execute_task(self, task: Task, request: ProjectRequest) -> List[Artifact]:
        logger.info(f"[{self.name}] Executando task especializada de backend: {task.name}")
        relevant_skills = ["api_design", "basic_coding"]
        task.skills = [s for s in task.skills if s in relevant_skills] or relevant_skills
        
        domain_rules = (
            "REGRAS DE BACKEND: Quando exigido, você deve gerar uma API funcional (preferencialmente FastAPI ou Flask). "
            "Crie um arquivo de inicialização claro (main.py ou app.py). "
            "Organize rotas, e defina schemas de request/response estritos usando Pydantic. "
            "Integre a camada de backend com o banco de dados utilizando os schemas e conexões previamente fornecidos."
        )
        task.description = f"{task.description}\n\n{domain_rules}{inject_dependencies(task, request)}"
        
        artifacts = super().execute_task(task, request)
        
        if not any(a.name.endswith('.py') for a in artifacts):
            raise ValueError(f"[{self.name}] Falha na validação: Nenhum código de backend (.py) foi gerado.")
            
        return artifacts


class FrontendAgent(BaseAgent):
    def execute_task(self, task: Task, request: ProjectRequest) -> List[Artifact]:
        logger.info(f"[{self.name}] Executando task especializada de frontend: {task.name}")
        relevant_skills = ["api_design", "basic_coding"]
        task.skills = [s for s in task.skills if s in relevant_skills] or relevant_skills
        
        domain_rules = (
            "REGRAS DE FRONTEND: Quando aplicável, gere uma estrutura web funcional. "
            "Se for um app completo, use React/Vite com package.json válido. Se for um Dashboard analítico, use Streamlit ou Dash. "
            "O frontend deve conter componentes de UI estruturados e se conectar aos endpoints da API ou dados analíticos fornecidos no contexto."
        )
        task.description = f"{task.description}\n\n{domain_rules}{inject_dependencies(task, request)}"
        
        artifacts = super().execute_task(task, request)
        
        if not any(a.name.endswith('.js') or a.name.endswith('.ts') or a.name.endswith('.tsx') or a.name.endswith('.jsx') or a.name.endswith('package.json') or a.name.endswith('.py') for a in artifacts):
            raise ValueError(f"[{self.name}] Falha na validação: Nenhum código ou configuração de frontend foi gerado.")
            
        return artifacts
