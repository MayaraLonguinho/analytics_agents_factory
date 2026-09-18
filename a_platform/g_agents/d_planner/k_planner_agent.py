import logging
import json
import re
import asyncio
from a_platform.b_contracts.e_execution_context import ExecutionContext
from a_platform.b_contracts import ProjectTask
from a_platform.c_brain.d_domains.a_domain_registry import DomainRegistry
from a_platform.i_llm_gateway.d_gateway import LLMGateway

logger = logging.getLogger(__name__)

class PlannerAgent:
    """
    Transforma as Decisões de Arquitetura e restrições de Domínio em um ProjectPlan executável completo via LLM.
    """
    def __init__(self, registry: DomainRegistry):
        self.registry = registry
        self.gateway = LLMGateway()

    def generate_plan(self, request: ExecutionContext) -> bool:
        return asyncio.run(self._generate_plan_async(request))

    async def _generate_plan_async(self, request: ExecutionContext) -> bool:
        logger.info("[PlannerAgent] Iniciando estruturação do plano via LLM...")
        
        domain_name = request.domain
        if domain_name not in ["analytics", "data_engineering"]:
            logger.error(f"[PlannerAgent] Falha: Planner suporta apenas analytics e data_engineering. Recebido: {domain_name}")
            return False
            
        domain_config = self.registry.get_domain_config(domain_name)
        
        allowed_agents = domain_config.get("agents", [])
        allowed_skills = domain_config.get("skills", [])
        allowed_mcps = domain_config.get("mcps", [])
        
        # Etapa 7: Extrair lições aprendidas do KnowledgeRegistry
        from a_platform.c_brain.g_registry.a_knowledge_registry import KnowledgeRegistry
        k_registry = KnowledgeRegistry()
        learned_rules = k_registry.get_learned_rules_for_domain(domain_name)
        
        learned_rules_text = ""
        if learned_rules:
            learned_rules_text = "\nATENÇÃO - LIÇÕES APRENDIDAS DE FALHAS ANTERIORES NESTE DOMÍNIO:\n"
            for idx, rule in enumerate(learned_rules, 1):
                learned_rules_text += f"{idx}. Padrão de Erro: {rule.get('pattern')} -> Recomendação: {rule.get('recommendation')}\n"
        
        system_prompt = (
            "Você é o Planner Agent, um TPM e Arquiteto Técnico.\n"
            "Sua tarefa é criar um plano de execução detalhado (DAG de tarefas) para a fábrica construir o projeto especificado.\n"
            f"{learned_rules_text}\n"
            "O plano DEVE ser de ponta a ponta (E2E), específico para o domínio do projeto e organizado rigorosamente nas seguintes camadas:\n"
            "- **Data Layer:** Ingestão e pipeline ETL (agent: DataAgent, skills: [etl_scripting]). Artefatos obrigatórios: [pipeline.py ou etl.py].\n"
            "- **Database Layer:** Schemas DDL, tabelas, relacionamentos (agent: DatabaseAgent, skills: [sql_generation]). Artefatos obrigatórios: [schema.sql ou init.sql].\n"
            "- **Analytics Layer:** Queries analíticas, cálculo de métricas/KPIs (agent: AnalyticsAgent, skills: [sql_generation, basic_coding]). Artefatos obrigatórios: [kpi_queries.sql ou analytics.py].\n"
            "- **Backend Layer:** API REST com rotas, schemas e serviços (agent: BackendAgent, skills: [api_design, basic_coding]). Artefatos obrigatórios: [rotas, schemas, app.py].\n"
            "- **Frontend Layer:** Componentes UI/React, Dashboard interativo (agent: FrontendAgent, skills: [basic_coding]). Artefatos obrigatórios: [componentes, package.json].\n"
            "- **Testing Layer:** Testes unitários e de integração com pytest (agent: TestingAgent, skills: [basic_coding]). Artefatos obrigatórios: [tests/test_*.py].\n"
            "- **Infrastructure Layer:** Dockerfile, docker-compose.yml (agent: InfrastructureAgent, skills: [basic_coding]). Artefatos obrigatórios: [Dockerfile, docker-compose.yml].\n"
            "- **Documentation Layer:** README.md (agent: DocumentationAgent, skills: [basic_coding]). Artefatos obrigatórios: [README.md].\n"
            "\n"
            "É OBRIGATÓRIO condicionar as capacidades às necessidades reais do projeto e Architecture Decision:\n"
            "- Base mínima para ETL/Data Engineering: Data/ETL, Testing, Documentation, e Database APENAS quando necessário/solicitado.\n"
            "- Base mínima para Analytics: Data/ETL, Analytics, Testing, Documentation, e Database APENAS quando necessário/solicitado.\n"
            "- CONDICIONAIS: Dashboard, Backend, Frontend, Infrastructure/Docker APENAS devem ser incluídos se explicitamente escolhidos na Arquitetura ou Requisitos.\n"
            "- NÃO OBRIGUE Backend, Frontend ou Dashboard em um projeto que não os solicitou.\n"
            "Utilize SOMENTE os Agentes, Skills e MCPs permitidos. Cada tarefa DEVE ser associada a UM agente e pode chamar múltiplas skills válidas.\n"
            "As tarefas devem seguir uma ordem lógica rigorosa sem ciclos. A dependência de uma tarefa deve listar os IDs exatos das tarefas anteriores que devem terminar primeiro.\n"
            "MUITO IMPORTANTE: O array `expected_artifacts` DEVE listar explicitamente os nomes dos arquivos que a tarefa vai gerar (ex: `pipeline.py`). A fábrica falhará se não listá-los corretamente ou listar fictícios!\n"
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
            f"Dataset Profile: {json.dumps(request.dataset_profile, ensure_ascii=False)}\n"
            f"Brain Context: {json.dumps(request.brain_context, ensure_ascii=False)}\n"
            f"Architecture Decision: {json.dumps(request.architecture_decision, ensure_ascii=False)}\n"
            f"Agentes Permitidos: {allowed_agents}\n"
            f"Skills Permitidas: {allowed_skills}\n"
            f"MCPs Permitidos: {allowed_mcps}\n"
            f"{system_prompt}"
        )
        
        schema = {
            "type": "object",
            "properties": {
                "tasks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "agent": {"type": "string"},
                            "skills": {"type": "array", "items": {"type": "string"}},
                            "mcps": {"type": "array", "items": {"type": "string"}},
                            "dependencies": {"type": "array", "items": {"type": "string"}},
                            "expected_artifacts": {"type": "array", "items": {"type": "string"}},
                            "commands": {"type": "array", "items": {"type": "string"}},
                            "validators": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["id", "name", "agent", "expected_artifacts"]
                    }
                },
                "run_commands": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["tasks"]
        }
        
        try:
            response = await self.gateway.structured_output(prompt, schema)
            if not response or not response.content:
                logger.error("[PlannerAgent] Resposta vazia ou nula recebida do LLM Gateway.")
                return False
            data = json.loads(response.content)
        except Exception as e:
            logger.error(f"[PlannerAgent] Falha ao obter output estruturado do LLM: {e}")
            return False
            
        plan = []
        
        print(f"DEBUG DATA: {data}")
        for t_data in data.get("tasks", []):
            task = ProjectTask(
                task_id=t_data.get("task_id", t_data.get("id")),
                name=t_data.get("name"),
                description=t_data.get("description", ""),
                assigned_agent=t_data.get("assigned_agent", t_data.get("agent")),
                required_skills=t_data.get("required_skills", t_data.get("skills", [])),
                required_mcps=t_data.get("required_mcps", t_data.get("mcps", [])),
                dependencies=t_data.get("dependencies", []),
                expected_artifacts=t_data.get("expected_artifacts", []),
                commands=t_data.get("commands", []),
                validators=t_data.get("validators", [])
            )
            plan.append(task)
            
        request.metadata["run_commands"] = data.get("run_commands", [])
        
        from a_platform.e_skills.h_registry.a_skill_registry import SkillRegistry
        from a_platform.g_agents.n_factory.a_agent_factory import AgentFactory
        
        skill_registry = SkillRegistry()
        agent_factory = AgentFactory()
        
        valid_task_ids = set()
        
        for task in plan:
            if not task.assigned_agent or task.assigned_agent not in allowed_agents:
                logger.error(f"[PlannerAgent] Agente inválido ou não autorizado: {task.assigned_agent}")
                return False
                
            for skill in task.required_skills:
                if skill not in allowed_skills or skill_registry.get_skill(skill) is None:
                    logger.error(f"[PlannerAgent] Skill inválida, ausente ou não autorizada: {skill}")
                    return False
                    
            valid_task_ids.add(task.task_id)

        for task in plan:
            for dep in task.dependencies:
                if dep not in valid_task_ids:
                    logger.error(f"[PlannerAgent] Dependência inválida: {dep} na tarefa {task.task_id}")
                    return False
        
        if not plan:
            logger.error("[PlannerAgent] Plano gerado está vazio. Falha na validação do plano.")
            return False
            
        if not hasattr(request, "project_context") or request.project_context is None:
            from a_platform.b_contracts.a_project import ProjectContext
            request.project_context = ProjectContext(project_id=request.project_id, project_name=request.project_id, project_path="")
        request.project_context.plan = plan
        
        logger.info(f"[PlannerAgent] Plano estruturado com sucesso via LLM. Total de tarefas: {len(plan)}")
        return True
