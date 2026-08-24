import logging
import json
import re
from a_platform.a_core.b_domain.project_request import ProjectRequest
from a_platform.a_core.b_domain.project_plan import ProjectPlan, Task
from a_platform.h_domains.domain_registry import DomainRegistry
from a_platform.f_llm_gateway.gateway import LLMGateway

logger = logging.getLogger(__name__)

class PlannerAgent:
    """
    Transforma as Decisões de Arquitetura e restrições de Domínio em um ProjectPlan executável completo via LLM.
    """
    def __init__(self, registry: DomainRegistry):
        self.registry = registry
        self.gateway = LLMGateway()

    def generate_plan(self, request: ProjectRequest) -> bool:
        logger.info("[PlannerAgent] Iniciando estruturação do plano via LLM...")
        
        domain_name = request.discovery_data.get("domain", "generic")
        domain_config = self.registry.get_domain_config(domain_name)
        
        allowed_agents = domain_config.get("agents", [])
        allowed_skills = domain_config.get("skills", [])
        allowed_mcps = domain_config.get("mcps", [])
        
        system_prompt = (
            "Você é o Planner Agent, um TPM e Arquiteto Técnico.\n"
            "Sua tarefa é criar um plano de execução detalhado (DAG de tarefas) para a fábrica construir o projeto especificado.\n"
            "O plano DEVE ser de ponta a ponta (E2E), específico para o domínio do projeto:\n"
            "- Se o domínio for 'Analytics': O plano DEVE conter Ingestão, Profiling, ETL, DB, Queries, Engine de Métricas, Testes e Infraestrutura.\n"
            "- Se for 'Ecommerce' ou 'CRM': O plano DEVE conter Modelagem de Banco, APIs, Lógica de Negócios e Testes.\n"
            "Utilize os Agentes, Skills e MCPs permitidos. Cada tarefa DEVE ser associada a UM agente e pode chamar múltiplas skills.\n"
            "As tarefas devem seguir uma ordem lógica rigorosa sem ciclos. A dependência de uma tarefa deve listar os IDs exatos das tarefas anteriores que devem terminar primeiro.\n"
            "Retorne APENAS um JSON válido no formato:\n"
            "{\n"
            '  "tasks": [\n'
            '    {\n'
            '      "id": "t_1",\n'
            '      "name": "Nome da Tarefa",\n'
            '      "description": "O que fazer",\n'
            '      "agent": "nome_do_agente",\n'
            '      "skills": ["skill_1", "skill_2"],\n'
            '      "mcps": ["mcp_1"],\n'
            '      "dependencies": [],\n'
            '      "expected_artifacts": ["app.py", "schema.sql"],\n'
            '      "commands": ["comando1"],\n'
            '      "validators": ["validator_pytest"]\n'
            '    }\n'
            '  ],\n'
            '  "run_commands": ["Comandos finais para executar o projeto"]\n'
            "}"
        )
        
        prompt = (
            f"Discovery Data: {json.dumps(request.discovery_data, ensure_ascii=False)}\n"
            f"Architecture Decision: {json.dumps(request.architecture_decision, ensure_ascii=False)}\n"
            f"Agentes Permitidos: {allowed_agents}\n"
            f"Skills Permitidas: {allowed_skills}\n"
            f"MCPs Permitidos: {allowed_mcps}\n"
        )
        
        response = self.gateway.generate(prompt, system_prompt=system_prompt, model_preference="openai")
        
        if not response.get("success"):
            logger.error(f"[PlannerAgent] LLM falhou ao gerar o plano: {response.get('error')}")
            return False
            
        text = response.get("text", "")
        json_str = text
        match = re.search(r'```(?:json)?(.*?)```', text, re.DOTALL)
        if match:
            json_str = match.group(1).strip()
            
        try:
            data = json.loads(json_str)
        except Exception as e:
            logger.error(f"[PlannerAgent] Falha ao parsear JSON do LLM: {e}\nRetorno: {text}")
            return False
            
        plan = ProjectPlan(
            project_id=request.project_id,
            domain=domain_name,
            materializer=domain_config.get("materializers", ["generic_materializer"])[0]
        )
        
        print(f"DEBUG DATA: {data}")
        for t_data in data.get("tasks", []):
            task = Task(
                id=t_data.get("id"),
                name=t_data.get("name"),
                description=t_data.get("description"),
                agent=t_data.get("agent"),
                skills=t_data.get("skills", []),
                mcps=t_data.get("mcps", []),
                dependencies=t_data.get("dependencies", []),
                expected_artifacts=t_data.get("expected_artifacts", []),
                commands=t_data.get("commands", []),
                validators=t_data.get("validators", [])
            )
            plan.add_task(task)
            
        plan.run_commands = data.get("run_commands", [])
        
        from a_platform.d_skills.skill_registry import SkillRegistry
        from a_platform.e_mcp.a_registry.mcp_registry import MCPRegistry
        from a_platform.c_agents.agent_factory import AgentFactory
        from a_platform.j_validation.validation_gate import ValidationGate
        
        if not plan.tasks:
            logger.error("[PlannerAgent] Plano gerado está vazio. Falha na validação do plano.")
            return False
            
        try:
            plan.validate_full(
                SkillRegistry(),
                MCPRegistry(),
                AgentFactory(),
                ValidationGate()
            )
        except ValueError as e:
            logger.error(f"[PlannerAgent] Validação profunda falhou: {e}")
            return False
            
        request.project_plan = plan
        
        logger.info(f"[PlannerAgent] Plano estruturado com sucesso via LLM. Total de tarefas: {len(plan.tasks)}")
        return True
