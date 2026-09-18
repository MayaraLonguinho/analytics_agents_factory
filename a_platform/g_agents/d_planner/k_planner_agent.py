import logging
import json
import re
import asyncio
from collections import defaultdict, deque
from typing import Set

from a_platform.b_contracts.e_execution_context import ExecutionContext
from a_platform.b_contracts import ProjectTask, ProjectPlan, ProjectContext
from a_platform.c_brain.d_domains.a_domain_registry import DomainRegistry
from a_platform.i_llm_gateway.d_gateway import LLMGateway
from a_platform.e_skills.h_registry.a_skill_registry import SkillRegistry
from a_platform.g_agents.n_factory.a_agent_factory import AgentFactory
from a_platform.f_mcps.d_registry.a_registry import MCPRegistry
from a_platform.j_runtime.b_command_policy.a_policy import CommandPolicy

logger = logging.getLogger(__name__)

# Agentes operacionais conhecidos pela AgentFactory
KNOWN_AGENTS: Set[str] = {
    "DataAgent",
    "DatabaseAgent",
    "AnalyticsAgent",
    "TestingAgent",
    "DocumentationAgent",
    "InfrastructureAgent",
    "BackendAgent",
    "FrontendAgent",
    "ChatbotAgent"
}

# Comandos de clientes de banco incompatíveis com execução local SQLite / Python
INCOMPATIBLE_STACK_COMMANDS: Set[str] = {
    "sqlcmd", "psql", "mysql", "mongo", "mongosh"
}


class PlannerAgent:
    """
    Transforma as Decisões de Arquitetura e restrições de Domínio em um ProjectPlan executável completo via LLM.
    Aplica validação determinística de permissão/existência para Agents, Skills e MCPs,
    preflight de CommandPolicy e garantia de comandos de evidência de Qualidade/Testes.
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
        
        # Contrato canônico estrito — chaves obrigatórias validadas pelo DomainRegistry
        allowed_agents = domain_config["allowed_agents"]
        allowed_skills = domain_config["allowed_skills"]
        allowed_mcps = domain_config["allowed_mcps"]
        
        system_prompt = (
            "Você é o Planner Agent, um TPM e Arquiteto Técnico.\n"
            "Sua tarefa é criar um plano de execução detalhado (DAG de tarefas) para a fábrica construir o projeto especificado.\n"
            "O plano DEVE ser de ponta a ponta (E2E), específico para o domínio do projeto e organizado rigorosamente nas seguintes camadas:\n"
            "- **Data Layer:** Ingestão e pipeline ETL (agent: DataAgent, skills: [etl_scripting]). Artefatos obrigatórios: [pipeline.py ou etl.py].\n"
            "- **Database Layer:** Schemas DDL, tabelas, relacionamentos (agent: DatabaseAgent, skills: [sql_generation]). Artefatos obrigatórios: [schema.sql ou init.sql].\n"
            "- **Analytics Layer:** Queries analíticas, cálculo de métricas/KPIs (agent: AnalyticsAgent, skills: [sql_generation, basic_coding]). Artefatos obrigatórios: [kpi_queries.sql ou analytics.py].\n"
            "- **Testing Layer:** Testes unitários e de integração com pytest (agent: TestingAgent, skills: [basic_coding, testing]). Artefatos obrigatórios: [tests/test_*.py].\n"
            "- **Documentation Layer:** README.md (agent: DocumentationAgent, skills: [basic_coding, documentation]). Artefatos obrigatórios: [README.md].\n"
            "\n"
            "REGRAS CRÍTICAS DE ARQUITETURA E COMANDOS:\n"
            "1. Todas as tarefas e comandos devem ser 100% compatíveis com a ArchitectureDecision e o ecossistema Python local.\n"
            "2. Para bancos relacionais como SQLite, qualquer manipulação ou criação de schema deve ser executada através de scripts Python (ex: 'python pipeline.py' ou 'python -m ...'). É TERMINANTEMENTE PROIBIDO propor comandos de clientes externos como 'sqlcmd', 'psql' ou 'mysql'.\n"
            "3. Todos os comandos devem obedecer à CommandPolicy da plataforma (executáveis permitidos: python, python3, pytest, flake8, ruff, bandit, pip, echo).\n"
            "4. A camada de testes e validação DEVE conter comandos reais de verificação: 'pytest tests/', 'flake8 .', 'bandit -r .' e 'pip check'.\n"
            "5. CONDICIONAIS: Dashboard, Backend web, Frontend ou Docker APENAS devem ser incluídos se explicitamente solicitados nos requisitos.\n"
            "6. Utilize SOMENTE os Agentes, Skills e MCPs permitidos listados abaixo. Cada tarefa DEVE ser associada a UM agente e pode chamar múltiplas skills válidas.\n"
            "7. As tarefas devem seguir uma ordem lógica rigorosa sem ciclos. A dependência de uma tarefa deve listar os IDs exatos das tarefas anteriores que devem terminar primeiro.\n"
            "8. O array `expected_artifacts` DEVE listar explicitamente os nomes dos arquivos que a tarefa vai gerar. A fábrica falhará se não listá-los corretamente!\n"
            "Retorne APENAS um JSON válido no formato:\n"
            "{\n"
            '  "tasks": [\n'
            '    {\n'
            '      "id": "t_1",\n'
            '      "name": "Nome da Tarefa",\n'
            '      "description": "O que fazer",\n'
            '      "agent": "nome_do_agente",\n'
            '      "skills": ["skill_1"],\n'
            '      "mcps": ["mcp_1"],\n'
            '      "dependencies": [],\n'
            '      "expected_artifacts": ["pipeline.py"],\n'
            '      "commands": ["python pipeline.py"],\n'
            '      "validators": ["validator_pytest"]\n'
            '    }\n'
            '  ],\n'
            '  "run_commands": ["Comandos finais para executar e validar o projeto"]\n'
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
            
        if not plan:
            logger.error("[PlannerAgent] Plano gerado está vazio. Falha na validação do plano.")
            return False

        skill_registry = SkillRegistry()
        agent_factory = AgentFactory()
        mcp_registry = MCPRegistry()
        
        valid_task_ids = set()
        
        # 1. Validação em Duas Dimensões: Permissão (Domain) + Existência (Registry/Factory)
        for task in plan:
            # --- Validação do Agente ---
            agent_id = task.assigned_agent
            if not agent_id or agent_id not in allowed_agents:
                logger.error(f"[PlannerAgent] Permissão negada: Agente '{agent_id}' não autorizado pelo domínio '{domain_name}'. Permitidos: {allowed_agents}")
                return False
                
            if agent_id not in KNOWN_AGENTS or agent_factory.get_agent(agent_id) is None:
                logger.error(f"[PlannerAgent] Existência inválida: Agente '{agent_id}' não pode ser resolvido operacionalmente pela AgentFactory.")
                return False
                
            # --- Validação das Skills ---
            for skill in task.required_skills:
                if skill not in allowed_skills:
                    logger.error(f"[PlannerAgent] Permissão negada: Skill '{skill}' não autorizada pelo domínio '{domain_name}'. Permitidas: {allowed_skills}")
                    return False
                    
                if skill_registry.get_skill(skill) is None:
                    logger.error(f"[PlannerAgent] Existência inválida: Skill '{skill}' não encontrada no SkillRegistry operacional.")
                    return False
                    
            # --- Validação dos MCPs ---
            for mcp in task.required_mcps:
                if mcp not in allowed_mcps:
                    logger.error(f"[PlannerAgent] Permissão negada: MCP '{mcp}' não autorizado pelo domínio '{domain_name}'. Permitidos: {allowed_mcps}")
                    return False
                    
                if mcp_registry.get_mcp(mcp) is None:
                    logger.error(f"[PlannerAgent] Existência inválida: MCP '{mcp}' não encontrado no MCPRegistry operacional.")
                    return False
                    
            valid_task_ids.add(task.task_id)

        # 2. Validação de Dependências e Integridade Referencial
        for task in plan:
            for dep in task.dependencies:
                if dep not in valid_task_ids:
                    logger.error(f"[PlannerAgent] Dependência inválida: '{dep}' referenciada na tarefa '{task.task_id}' não existe no plano.")
                    return False

        # 3. Detecção Determinística de Ciclos (DAG check)
        graph = defaultdict(list)
        in_degree = defaultdict(int)
        for t in plan:
            in_degree[t.task_id] = 0
        for t in plan:
            for dep in t.dependencies:
                graph[dep].append(t.task_id)
                in_degree[t.task_id] += 1
        queue = deque([tid for tid in in_degree if in_degree[tid] == 0])
        visited_count = 0
        while queue:
            curr_id = queue.popleft()
            visited_count += 1
            for neighbor in graph[curr_id]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        if visited_count != len(plan):
            logger.error("[PlannerAgent] Dependências circulares detectadas nas tarefas do plano.")
            return False

        # 4. Preflight de Comandos e Compatibilidade com a ArchitectureDecision
        raw_run_commands = data.get("run_commands", [])
        all_planned_commands = []
        for t in plan:
            all_planned_commands.extend(t.commands)
        all_planned_commands.extend(raw_run_commands)

        valid_run_commands = []
        for cmd in all_planned_commands:
            valid, msg, args = CommandPolicy.parse_and_validate(cmd)
            if not valid:
                logger.error(f"[PlannerAgent] Preflight CommandPolicy falhou para o comando '{cmd}': {msg}")
                return False
                
            base_exe = args[0].lower() if args else ""
            if base_exe in INCOMPATIBLE_STACK_COMMANDS:
                logger.error(
                    f"[PlannerAgent] Comando '{cmd}' incompatível com a ArchitectureDecision da stack (SQLite/Python). "
                    f"Executáveis de cliente externo como '{base_exe}' são proibidos; utilize scripts Python locais."
                )
                return False

        # 5. Garantia de Comandos e Evidências Obrigatórias para Quality & Validation
        # Downstream gates requerem: pytest (testes), flake8/ruff (CodeQuality), bandit (SecurityQuality), pip check (DependencyQuality)
        for cmd in raw_run_commands:
            valid, _, _ = CommandPolicy.parse_and_validate(cmd)
            if valid and cmd not in valid_run_commands:
                valid_run_commands.append(cmd)

        has_pytest = any("pytest" in c for c in valid_run_commands)
        has_cq = any(c.startswith(("flake8", "ruff")) for c in valid_run_commands)
        has_sq = any("bandit" in c for c in valid_run_commands)
        has_dq = any("pip check" in c for c in valid_run_commands)

        if not has_pytest:
            valid_run_commands.append("pytest tests/")
        if not has_cq:
            valid_run_commands.append("flake8 .")
        if not has_sq:
            valid_run_commands.append("bandit -r .")
        if not has_dq:
            valid_run_commands.append("pip check")

        request.metadata["run_commands"] = valid_run_commands

        # 6. Atualizar ProjectContext e ProjectPlan com o plano validado
        if not hasattr(request, "project_context") or request.project_context is None:
            request.project_context = ProjectContext(project_id=request.project_id, project_name=request.project_id, project_path="")
        request.project_context.plan = plan
        
        request.project_plan = ProjectPlan(
            project_id=request.project_id,
            domain=domain_name,
            tasks=plan,
            run_commands=valid_run_commands
        )
        
        logger.info(f"[PlannerAgent] Plano estruturado e validado com sucesso. Total de tarefas: {len(plan)}. Comandos de execução/qualidade planejados: {len(valid_run_commands)}")
        return True
